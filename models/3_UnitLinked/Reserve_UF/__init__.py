from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def ACCM_FV(t):

    """Accumulated fund value for calculation of
    2-year average fund value required for
    loyalty bonus calculations"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return (ACCM_FV(t-1) + AV_PP_AT(t, "BEF_PW_LB")) * (Proj.DUR_M(t) <= Proj.POL_TERM_M())


def ALLOC_CHARGE_RATE(t):

    """Allocation charge rates used for projection"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        n = Input.AllocCharge["Reserving"].index.max()
        dur = list(Input.np.minimum(Proj.DUR_Y(t), n))
        return Input.pd.Series(list(Input.AllocCharge["Reserving"][dur]), index = Proj.MP().index)


def AVG_2Y(t, var: str):

    """Returns the 2-year average of the variable passed"""    

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    if t <= 24:
        return eval(f"{var}({t})") / t
    else:
        return (eval(f"{var}({t})")-eval(f"{var}({t-24})")) / 24


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
        return AV_PP_AT(t-1, "END") * (Proj.DUR_M(t)<=Proj.POL_TERM_M())

    elif timing == "BEF_FEE":
        return AV_PP_AT(t, "START") + PREM_TO_AV_PP(t)

    elif timing == "BEF_INV":
        return AV_PP_AT(t, "BEF_FEE") - CHG_ADMIN(t) - CHG_MORT(t)

    elif timing == "BEF_PW_LB":
        return AV_PP_AT(t, "BEF_INV")  + INV_INC_PP(t) - CHG_FMC(t)

    elif timing == "END":
        return AV_PP_AT(t, "BEF_PW_LB")  - PW(t) + LOYALTY(t)

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
    FV > charge => min(charge*premium*(1+tax), charge_Cap(1+tax))"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        Charge = Input.ADMIN_CHARGE_RATE(t) * Proj.MP()["ann_prem"] * (1 + Input.ST_rate["Allocation/Admin Charge"])
        Cap = Input.admin_chg_cap["Cap"] * (1+Input.ST_rate["Allocation/Admin Charge"])

        return Input.np.minimum(AV_PP_AT(t, "BEF_FEE"), Input.np.minimum(Cap, Charge)) * (Proj.DUR_M(t) <= Proj.POL_TERM_M())


def CHG_ALLOC(t):

    """Allocation Charge"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        flag = (Proj.DUR_M(t) <= Proj.PREM_TERM_M()) * ((Proj.DUR_M(t)-1)/12 == Proj.DUR_Y(t) - 1)
        return ALLOC_CHARGE_RATE(t) * Proj.PREM_PP() * (1 + Input.ST_rate["Allocation/Admin Charge"]) * flag


def CHG_FMC(t):

    """Fund management charge"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return (AV_PP_AT(t, "BEF_INV") + INV_INC_PP(t)) * Input.res_UF_FMC["FMC"]/12 * (1 + Input.ST_rate["FMC"]) * (Proj.DUR_M(t) <= Proj.POL_TERM_M())


def CHG_MORT(t):

    """Mortality charge"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        mort= Input.CHG_MORT_RATE(t-1) * Proj.MP()["mort_loading"]
        scale = Input.mort_chg_scale["Male"] * (Proj.SEX() == "M") + Input.mort_chg_scale["Female"] * (Proj.SEX() == "F")
        return (SAR(t) * mort * scale)/12 * (1+Input.ST_rate["Mortality Charge"]) * (Proj.DUR_M(t) <= Proj.POL_TERM_M())


def INV_INC_PP(t):

    """Investment income on account value per policy

    Investment income on account value defined as::

        inv_return_mth(t) * av_pp_at(t, "BEF_INV")"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        dur = Input.np.ceil(t/12)
        inv_rate_mth = (1 + Input.res_UF_FMC["Unit Growth"]) ** (1/12) - 1
        return (inv_rate_mth * AV_PP_AT(t, "BEF_INV")) * (Proj.DUR_M(t) <= Proj.POL_TERM_M())


def LOYALTY(t):

    """Loyalty bonus"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        flag = (Proj.DUR_Y(t) == Proj.DUR_M(t)/12) * (Proj.DUR_M(t) <= Proj.POL_TERM_M())
        return flag *  AVG_2Y(t, "ACCM_FV") * Input.LOYALTY_RATE(t)


def PREM_TO_AV_PP(t):

    """Per-policy premium portion put in the account value

    The amount of premium per policy net of loading,
    which is put in the accoutn value."""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return (Proj.PREM_PP() - CHG_ALLOC(t))*((Proj.DUR_M(t)-1)/12 == Proj.DUR_Y(t)-1)*(Proj.DUR_M(t)<=Proj.PREM_TERM_M())


def PW(t):

    """Partial Withdrawal per policy"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return (Proj.MP()['ann_prem'] * Input.np.minimum( Proj.DUR_Y(t), Proj.MP()["prem_paying_term"]) * PW_RATE(t)/12) * (Proj.DUR_M(t) <= Proj.POL_TERM_M())


def PW_RATE(t):

    """Partial Withdrawal Rates"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        n = Input.PartialWithdrawal["Reserving"].index.max()
        dur = list(Input.np.minimum(Proj.DUR_Y(t), n))
        return Input.pd.Series(list(Input.PartialWithdrawal["Reserving"][dur]), index = Proj.MP().index)


def SAR(t):

    """Sum at risk at time `t`"""

    if t < 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        if t == 0:
            av = AV_PP_INIT()
        else:
            av = AV_PP_AT(t, "BEF_FEE")
        return Input.np.maximum(0, Input.np.maximum(Proj.SUM_ASSURED(t) - Proj.DTH_BEN_RED(t), Proj.DTH_BEN_MIN(t)) - av * (1 - Proj.IND_DB())) * (Proj.DUR_M(t) <= Proj.POL_TERM_M())


def ST_ADMIN(t):

    """Service tax: administration charge"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return (CHG_ADMIN(t)/(1+Input.ST_rate["Allocation/Admin Charge"]) * Input.ST_rate["Allocation/Admin Charge"]) * (Proj.DUR_M(t) <= Proj.POL_TERM_M())


def ST_ALLOC(t):

    """Service tax: allocation charge"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return (CHG_ALLOC(t)/(1+Input.ST_rate["Allocation/Admin Charge"])*Input.ST_rate["Allocation/Admin Charge"]) * (Proj.DUR_M(t) <= Proj.POL_TERM_M())


def ST_FMC(t):

    """Service tax: fund management charge"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return (CHG_FMC(t)/(1+Input.ST_rate["FMC"])*Input.ST_rate["FMC"]) * (Proj.DUR_M(t) <= Proj.POL_TERM_M())


def ST_MORT(t):

    """Service tax: mortality charges"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return (CHG_MORT(t) /(1 + Input.ST_rate["Mortality Charge"]) *Input.ST_rate["Mortality Charge"]) * (Proj.DUR_M(t) <= Proj.POL_TERM_M())


# ---------------------------------------------------------------------------
# References

Input = ("Interface", ("..", "Input"), "auto")

Proj = ("Interface", ("..", "Projection"), "auto")