from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def COMM(t): 

    """Commissions:
        valuation basis"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        n = Input.comm_rates.index.max()
        dur_m = list(Input.np.minimum(Input.np.ceil(Proj.DUR_M(t)/12), n))
        comm_rates = Input.comm_rates["Reserves"][dur_m]

        return Proj.IND_ACTIVE(t) * PREM_PAYBL_M(t) * list(comm_rates)


def DISC_RATE_M(t):

    """Monthly discount rate adj for Inv expenses:
        valuation basis"""

    return (1 + Input.res_IR["Reserve IR"] - Input.res_inv_exp_pc["Investment Expenses %"]) ** (1/12) - 1


def DTH_BEN(t):

    """Death benefit:
        valuation basis

        After allowing for Terminal bonus and declared bonus"""

    if t < 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return Proj.IND_ACTIVE(t) * (Input.np.maximum(Input.np.maximum(Proj.SUM_ASSURED(), 10 * Proj.PREM_PP()), Proj.DUR_M(t) * 1.05 * (Proj.PREM_PP() / 12)) 
                                     + cob.RES_DECLRD_REV_BONUS(t) 
                                     + TERMINAL_BON(t)) * POLS_DTH(t)


def EXPS(t):

    """Total expenses:
        valuation basis

        Accounting for acquisition, maintenance
        and claim expenses:"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        acq   = EXPS_ACQ(t) * (Proj.DUR_M(t-1) == 0)
        maint = EXPS_MAINT(t)
        claim = EXPS_CLAIM(t) 
        return (Proj.DUR_M(t) <= Proj.POL_TERM_M()) * (acq + maint + claim)


def EXPS_ACQ(t):

    """Acquisition expense per policy:
        valuation basis"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        i        = Input.exp_acq["Fixed"]
        per_prem = Input.exp_acq["% of Premium"]
        per_sa   = Input.exp_acq["% of SA"]

        exp_acq = i + per_prem * Proj.PREM_PP() + per_sa * Proj.SUM_ASSURED()
        return exp_acq * (1 + Input.mad["Expense"]) * (Proj.DUR_M(t-1) == 0)


def EXPS_CLAIM(t):

    """Expenses incured at death/surrender/maturity:
        valuation basis"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
       return Input.pd.Series(0, index = Proj.MP().index)
    else:
       return Proj.IND_ACTIVE(t) * Input.exp_claim["Claims"] * INFL_FAC(t) * (1 + Input.mad["Expense"]) * (POLS_DTH(t) + POLS_LAPSE(t) * (Proj.DUR_M(t) > Input.surr_start_term["Surrender Start"]))


def EXPS_MAINT(t):

    """Annual maintenance expense per policy:
        valuation basis"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        e           = Input.res_exp_maint["Fixed"]/12 * INFL_FAC(t)
        per_prem    = Input.res_exp_maint["% of Premium"]
        flag        = (Proj.DUR_M(t-1) > 0) * Proj.IND_ACTIVE(t)

        return flag * (e + per_prem * Proj.PREM_PP()/12) * (1 + Input.mad["Expense"]) * POLS_IF(t-1)


def GROSS_TRNS_SH(t):

    """Gross Transfer to Shareholders"""

    if t <= 0 or t > Proj.PROJ_LEN().max():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return (POLS_IF(t) * cob.RES_COB_PP(t) 
                + TERMINAL_BON(t) * POLS_DTH(t) 
                + (Proj.DUR_M(t) == Proj.POL_TERM_M())* POLS_IF(t) * TERMINAL_BON(t)) * Input.sh_prop["Share"] / (1 - Input.sh_prop["Share"]) / (1 - Input.Tax_Rates["Shareholder"])


def INFL_FAC(t):

    """The inflation factor at time t:
        valuation basis"""

    if t < 0:
        raise ValueError("t cannot be less than 0.")
    elif t <= 1:
        return 1
    else:
        return (1 + INFL_RATE()) ** ((t-1)/12)


def INFL_RATE():

    """Inflation rate:
        valuation basis"""

    return Input.res_infl_rate["Inflation"]


def INT_NET_CF(t):

    """Interest earned on net cashflows:
        valuation basis"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return (PREM_PAYBL_M(t)
                - EXPS_ACQ(t)
                - EXPS_MAINT(t)
                - COMM(t)
                - MAT_BEN(t)) * Proj.IND_ACTIVE(t) * DISC_RATE_M(t)


def LAPSE_RATE(t):

    """Lapse rate:
        valuation basis"""

    return Proj.LAPSE_RATE(t) * (1 + Input.mad["Lapse"])


def MAT_BEN(t):

    """Maturity benefit:
        Valuation basis"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0,index = Proj.MP().index)
    else:
        return (Proj.DUR_M(t) == Proj.POL_TERM_M() + 1) * (Proj.SUM_ASSURED() + cob.RES_DECLRD_REV_BONUS(t-1)+ TERMINAL_BON(t-1)) * POLS_MAT(t-1)


def MORT_RATE_ANN(t):

    """Mortality rate to be applied at time t:
        valuation basis"""

    fac = Input.res_mort_scale["Rate"]
    return fac * Input.BASE_MORT_RATE(t)


def MORT_RATE_MLY(t):

    """Monthly mortality rate to be applied at time t:
        valuation basis"""

    return 1 - (1 - MORT_RATE_ANN(t))**(1/12)


def NET_CF(t):

    """Net cashflow:
        valuation basis"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return (PREM_PAYBL_M(t)
            + INT_NET_CF(t)
            - DTH_BEN(t)
            - EXPS(t)
            - COMM(t)
            - SURR_BEN(t)
            - MAT_BEN(t)
            - GROSS_TRNS_SH(t)
            - TAX_SH_PH_TRNS(t)) * (Proj.DUR_M(t) <= Proj.POL_TERM_M()+1)


def POLS_DTH(t):

    """Number of death occurring at time t:
        valuation basis"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        flag = Proj.DUR_M(t) <= Input.surr_start_term["Surrender Start"]
        return Proj.IND_ACTIVE(t) * POLS_IF(t - 1) * MORT_RATE_MLY(t) * (flag + (1 - flag) * (1 - LAPSE_RATE_MLY(t)/2))


def POLS_IF(t):

    """Number of policies in-force:
        valuation basis

    The initial value is read from :func:`pols_if_init`.
    Subsequent values are defined recursively."""

    if t < 0:
        raise ValueError("t cannot be less than 0")
    elif t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    elif t == 0:
        return Proj.INIT_POLS_IF()
    else:
        return Proj.IND_ACTIVE(t) * (POLS_IF(t-1) - POLS_DTH(t) - POLS_LAPSE(t))


def POLS_LAPSE(t):

    """Number of lapse occurring at time t:
        valuation basis"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return Proj.IND_ACTIVE(t) * POLS_IF(t-1) * (1 - MORT_RATE_MLY(t)) * LAPSE_RATE_MLY(t)


def POLS_MAT(t):

    """Number of maturing policies:
        valuation basis

    The policy maturity occurs at ``t == 12 * policy_term()``,
    after death and lapse during the last period::

    otherwise ``0``."""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return (Proj.DUR_M(t) == Proj.POL_TERM_M()) * POLS_IF(t)


def PREM_PAYBL_M(t):

    """Premium income:
        valuation basis

    Premium income during the period from ``t`` to ``t+1`` defined as::

        premium_pp(t) * pols_if(t)"""

    if t < 0:
        raise ValueError("t cannot be less than 0.")
    elif t == 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return (Proj.DUR_M(t) <= Proj.PREM_TERM_M()) * Proj.PREM_PP()/12 * POLS_IF(t-1)


def RESERVE(t):

    """Reserve calculation

    Reserve value at the period ``t`` is defined as::
        (reserve(t+1) - net_cf(t+1)) / (1 + disc_rate_mth())"""

    if t < 0:
        raise ValueError("t cannot be less than 0.")
    elif t == 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return Proj.IND_ACTIVE(t) * (RESERVE(t+1) - NET_CF(t+1)) / (1 + DISC_RATE_M(t))


def RESERVE_PP(t):

    """Reserve value per policy
    Reserve value per policy at the period ``t`` is defined as::

        reserve(t) / pols_if(t)"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        res = Input.np.array([RESERVE(t)], dtype = float)
        pols = Input.np.array([POLS_IF(t)], dtype = float)
        res_pp = Input.np.divide(res, pols, out = Input.np.zeros_like(res), where = pols!= 0)

        return Input.np.maximum(SURR_VAL(t), Input.pd.Series(sum(res_pp), index = Proj.MP().index))


def SURR_BEN(t):

    """Surrender benefit:
        valuation basis"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return SURR_VAL(t) * POLS_LAPSE(t)


def TAX_SH_PH_TRNS(t):

    """Tax on ShareHolder and PolicyHolder Transfer"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return (POLS_IF(t) * cob.RES_COB_PP(t) 
                + TERMINAL_BON(t) * POLS_DTH(t)
                + (Proj.DUR_M(t) == Proj.POL_TERM_M()) * POLS_IF(t) * TERMINAL_BON(t)) * Input.Tax_Rates["Policyholder"] / (1-Input.Tax_Rates["Policyholder"])


def TERMINAL_BON(t):

    """Terminal Bonus Payable on Death"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        flag = Proj.IND_ACTIVE(t) * (Proj.DUR_M(t) >= 1)
        return flag * Input.term_bon_flag["Flag"] * Input.res_terminal_bonus_rt["Terminal"] * (Proj.SUM_ASSURED() + cob.RES_DECLRD_REV_BONUS(t))


def GSV(t):

    """Guaranteed Surrender Value
        Valuation Basis"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        flag = (Proj.DUR_M(t) > Input.surr_start_term["Surrender Start"])
        return flag * (Input.ACB_FAC(t) * cob.RES_DECLRD_REV_BONUS(t) + (Proj.DUR_M(t)/12) * Input.GSV_FAC(t) * Proj.PREM_PP())


def SSV(t):

    """Special Surrender Values
        Valuation Basis"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return Proj.IND_ACTIVE(t) * (Proj.DUR_M(t) > Input.surr_start_term["Surrender Start"]) * (Proj.PV_DB(t) + Proj.PV_MAT_BEN(t)) * ((Proj.DUR_M(t)/(Proj.PREM_TERM_Y()*12)) * Proj.SUM_ASSURED() + cob.RES_DECLRD_REV_BONUS(t))


def SURR_VAL(t):

    """Surrender value
        defined as: Max(SSV, GSV)"""

    return Input.np.maximum(SSV(t), GSV(t)) * (Proj.DUR_M(t) > Input.surr_start_term["Surrender Start"])


def LAPSE_RATE_MLY(t):

    """Monthly lapse rate to be applied at time t:
        valuation basis"""

    return 1 - (1 - LAPSE_RATE(t)) ** (1/12)


# ---------------------------------------------------------------------------
# References

Proj = ("Interface", ("..", "Projection"), "auto")

Input = ("Interface", ("..", "Input"), "auto")

cob = ("Interface", ("..", "COBFactor"), "auto")