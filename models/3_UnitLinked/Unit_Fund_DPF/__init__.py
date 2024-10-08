from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def AV_PP_AT(t, timing):

    """START , BEF_FEE, BEF_INV, BEF_PW_LB, END"""
    """Account value per policy

    :func:`av_at(t, timing)<av_at>` calculates
    the total amount of account value at time ``t`` for the policies in-force.

    At each ``t``, the events that change the account value balance
    occur in the following order:

        * Premium payment
        * Fee deduction

    Investment income is assumed to be earned throughout each month,
    so at the middle of the month when death and lapse occur,
    half the investment income for the month is credited.

    The second parameter ``timing`` takes a string to
    indicate the timing of the account value, which is either
    ``"START"``, ``"BEF_FEE"``, ``"BEF_INV"`` or ``"END"``.

    .. rubric:: START
    Account value before premium payment.

    .. rubric:: BEF_FEE
    Account value after premium payment before fee deduction

    .. rubric:: BEF_INV
    Account value after fee deduction before crediting investemnt return

    .. rubric:: BEF_PW_LB
    Account value after crediting investment return

    .. rubric:: END
    Account value at the end of the time `t`
    At the start of the projection (i.e. when ``t=0``),
    the account value is set to :func:`av_pp_init`.

    NOTE: for functions such as this, the first part of
    documentation should be the arguments to this function
    for Output.RESULTS function to run properly"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        if t == 0 and timing == "END":
            return AV_PP_INIT()
        else:
            return Input.pd.Series(0, index = Proj.MP().index)

    elif timing == "START":
        return AV_PP_AT(t-1, "END") * (Proj.DUR_M(t)<= Input.surr_mth["Surrender Month"])

    elif timing == "BEF_FEE":
        return AV_PP_AT(t, "START") 

    elif timing == "BEF_INV":
        return AV_PP_AT(t, "BEF_FEE") 

    elif timing == "BEF_PW_LB":
        return AV_PP_AT(t, "BEF_INV") + INV_INC_PP(t) - CHG_FMC(t)

    elif timing == "END":
        if t > Input.surr_mth["Surrender Month"]:
            return Input.pd.Series(0, index = Proj.MP().index)

        elif t == Input.surr_mth["Surrender Month"]:
            return AV_PP_AT(t, "BEF_PW_LB")

        else:
            surr_charge = Input.np.minimum(Input.SURR_CHG_RATE(t) * Input.np.minimum(Proj.PREM_PP(), UF.AV_PP_AT(t, "END")), Input.SURR_CHG_CAP(t))

            value = Input.np.array(AV_PP_AT(t, "BEF_PW_LB") * (Proj_DPF.POLS_IF(t) - Proj.POLS_LAPSE(t))
                                   + Proj.POLS_LAPSE(t) * (UF.AV_PP_AT(t, "END") - surr_charge))

            pols = Input.np.array(Proj_DPF.POLS_IF(t))

            end_val = Input.np.divide(value, pols, out = Input.np.zeros_like(value), where = pols!= 0)
            val = Input.pd.Series(list(end_val), index = Proj.MP().index)
            return val * (Proj_DPF.POLS_IF(t)>0)

    else:
        raise ValueError("invalid timing")


def AV_PP_INIT():

    """Initial account value per policy

    For existing business at time ``0``,
    returns initial per-policy accout value read from
    the ``av_pp_init`` column in :func:`model_point`.
    For new business, 0 should be entered in the column."""

    return Proj.MP()["FV_start"]


def CHG_ADMIN(t):

    """Maintenance fee per policy

    if FV < charge => FV
    FV > charge => min(charge*premium*(1+tax), charge_Cap(1+tax))
    """

    return Input.pd.Series(0, index = Proj.MP().index)


def CHG_ALLOC(t):

    """Allocation Charge"""

    return Input.pd.Series(0, index = Proj.MP().index)


def CHG_FMC(t):

    """Fund management charge"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return (AV_PP_AT(t, "BEF_INV") + INV_INC_PP(t)) * Input.UF_FMC["Disct Fund FMC"]/12 * (1 + Input.ST_rate["FMC"]) * (Proj.DUR_M(t) <= Proj.POL_TERM_M())


def CHG_MORT(t):

    """Mortality charges"""    

    return Input.pd.Series(0, index = Proj.MP().index)


def INV_INC_PP(t):

    """Investment income on account value per policy

    Investment income on account value defined as::

        inv_return_mth(t) * av_pp_at(t, "BEF_INV")"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        dur = Input.np.ceil(t/12)
        inv_rate_mth = (1 + Input.YieldCurve["Discount Rates"][dur]) ** (1/12) - 1
        return inv_rate_mth * AV_PP_AT(t, "BEF_INV") * (Proj.DUR_M(t) <= Proj.POL_TERM_M())


def PREM_TO_AV_PP(t):

    """Per-policy premium portion put in the account value

    The amount of premium per policy net of loading,
    which is put in the accoutn value."""

    return Input.pd.Series(0, index = Proj.MP().index)


def ST_ADMIN(t):

    """Service tax: administration charge"""

    return Input.pd.Series(0, index = Proj.MP().index)


def ST_ALLOC(t):

    """Service tax: allocation charge"""

    return Input.pd.Series(0, index = Proj.MP().index)


def ST_FMC(t):

    """Service tax: fund management charge"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return CHG_FMC(t)/(1 + Input.ST_rate["FMC"]) * Input.ST_rate["FMC"] * (Proj.DUR_M(t) <= Proj.POL_TERM_M())


def ST_MORT(t):

    """Service tax: mortality charge"""

    return Input.pd.Series(0, index = Proj.MP().index)


# ---------------------------------------------------------------------------
# References

Input = ("Interface", ("..", "Input"), "auto")

Proj = ("Interface", ("..", "Projection"), "auto")

Proj_DPF = ("Interface", ("..", "Projection_DPF"), "auto")

UF = ("Interface", ("..", "Unit_Fund"), "auto")