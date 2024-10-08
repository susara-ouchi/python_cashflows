from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def DTH_BEN(t):
    """Death claims:
        valuation basis"""

    return (Proj.DUR_M(t) <= Proj.POL_TERM_M()) * Proj.SUM_ASSURED() * POLS_DTH(t)


def COMM(t): 
    """Commissions:
        valuation basis"""

    if t <= 0:
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        n = Input.comm_rates.index.max()
        dur_m = list(Input.np.minimum(Input.np.ceil(Proj.DUR_M(t)/12), n))
        comm_rates = Input.comm_rates["Reserves"][dur_m]

        return (Proj.DUR_M(t) < Proj.POL_TERM_M()) * PREM_PAYBL_M(t) * list(comm_rates)


def EXPS_ACQ(t):
    """Acquisition expense per policy:
        valuation basis"""

    if t <= 0:
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        i        = Input.exp_acq["Fixed"]
        per_prem = Input.exp_acq["% of Premium"]
        per_sa   = Input.exp_acq["% of SA"]

        exp_acq = i + per_prem * Proj.PREM_PP() + per_sa * Proj.SUM_ASSURED()
        return exp_acq * (1 + Input.mad["Expense"]) * (Proj.DUR_M(t-1) == 0)


def EXPS_MAINT(t):
    """Annual maintenance expense per policy:
        valuation basis"""

    if t <= 0:
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        e           = Input.exp_maint["Fixed"]/12 * INFL_FAC(t-1)
        per_prem    = Input.exp_maint["% of Premium"]
        flag        = (Proj.DUR_M(t-1) > 0) * (Proj.DUR_M(t) <= Proj.POL_TERM_M())

        return flag * (e + per_prem * Proj.PREM_PP()/12) * (1 + Input.mad["Expense"]) * POLS_IF(t-1)


def EXPS_CLAIM(t):
    """Expenses incured at death/surrender/maturity:
        valuation basis"""

    return ( (Proj.DUR_M(t) <= Proj.POL_TERM_M()) * Input.exp_claim["Claims"] * INFL_FAC(t) * (1 + Input.mad["Expense"])
            * (POLS_DTH(t) + POLS_LAPSE(t) * (SURR_BEN(t) > 0) + POLS_MAT(t)) )


def EXPS(t):
    """Total expenses:
        valuation basis

        Accounting for acquisition, maintenance
        and claim expenses:"""

    if t <= 0:
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        acq   = EXPS_ACQ(t) * (Proj.DUR_M(t-1) == 0)
        maint = EXPS_MAINT(t)
        claim = EXPS_CLAIM(t) 
        return (Proj.DUR_M(t) <= Proj.POL_TERM_M()) * (acq + maint + claim)


def INFL_FAC(t):
    """The inflation factor at time t:
        valuation basis"""

    if t < 0:
        raise ValueError
    else:
        return (1 + INFL_RATE())**(t/12)


def INFL_RATE():
    """Inflation rate:
        valuation basis"""

    return Input.res_infl_rate["Inflation"]


def LAPSE_RATE(t):
    """Lapse rate:
        valuation basis"""

    return Proj.LAPSE_RATE(t)*(1 + Input.mad["Lapse"])


def MORT_RATE_ANN(t):
    """Mortality rate to be applied at time t:
        valuation basis"""

    fac = Input.res_mort_scale["Rate"]
    return fac * Proj.BASE_MORT_RATE(t)


def MORT_RATE_MLY(t):
    """Monthly mortality rate to be applied at time t:
        valuation basis"""

    return 1 - (1 - MORT_RATE_ANN(t))**(1/12)


def NET_CF(t):
    """Net cashflow:
        valuation basis"""

    if t <= 0:
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return (PREM_PAYBL_M(t)
            + INT_NET_CF(t)
            - DTH_BEN(t)
            - EXPS(t)
            - COMM(t)
            - SURR_BEN(t)
            - MAT_BEN(t)
            - INCM_BEN(t)) * (Proj.DUR_M(t) <= Proj.POL_TERM_M())


def POLS_IF(t):
    """Number of policies in-force:
        valuation basis

    The initial value is read from :func:`pols_if_init`.
    Subsequent values are defined recursively."""

    if t == 0:
        return Proj.INIT_POLS_IF()
    elif t < 0:
        raise ValueError
    else:
        return (Proj.DUR_M(t) <= Proj.POL_TERM_M()) * (POLS_IF(t-1) - POLS_DTH(t) - POLS_LAPSE(t))


def POLS_DTH(t):
    """Number of death occurring at time t:
        valuation basis"""

    if t <= 0:
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return (Proj.DUR_M(t) <= Proj.POL_TERM_M()) * POLS_IF(t - 1) * MORT_RATE_MLY(t)


def POLS_LAPSE(t):
    """Number of lapse occurring at time t:
        valuation basis"""

    if t <= 0:
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return (Proj.DUR_M(t) <= Proj.POL_TERM_M()) * (POLS_IF(t - 1) - POLS_DTH(t)) * (1-(1 - LAPSE_RATE(t))**(1/12))


def POLS_MAT(t):
    """Number of maturing policies:
        valuation basis

    The policy maturity occurs at ``t == 12 * policy_term()``,
    after death and lapse during the last period::

        pols_if(t-1) - pols_lapse(t-1) - pols_death(t-1)

    otherwise ``0``."""

    return (Proj.DUR_M(t) == Proj.POL_TERM_M()) * POLS_IF(t)


def PREM_PAYBL_M(t):
    """Premium income:
        valuation basis

    Premium income during the period from ``t`` to ``t+1`` defined as::

        premium_pp(t) * pols_if(t)"""

    if t < 0:
        raise ValueError("t cannot be less than 0.")
    elif t == 0:
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return (Proj.DUR_M(t) <= Proj.PREM_TERM_M()) * Proj.PREM_PP()/12 * POLS_IF(t-1)


def RESULT_CF():
    """Result table of cashflows"""

    t_len = range(Proj.PROJ_LEN().max())

    data = {
        "Premiums": [sum(PREM_PAYBL_M(t)) for t in t_len],
        "Claims": [sum(DTH_BEN(t)) for t in t_len],
        "Expenses": [sum(EXPS(t)) for t in t_len],
        "Commissions": [sum(COMM(t)) for t in t_len],
        "Int_Net_CF": [sum(INT_NET_CF(t)) for t in t_len],        
        "Net Cashflow": [sum(NET_CF(t)) for t in t_len]
    }

    dataframe = Input.pd.DataFrame.from_dict(data)

    return dataframe


def SURR_BEN(t):
    """Surrender benefit:
        valuation basis"""

    return Proj.SURR_VAL(t) * POLS_LAPSE(t)


def MAT_BEN(t):
    """Maturity benefit:
        valuation basis"""

    return Proj.TERMINAL_BEN() * POLS_MAT(t)


def INT_NET_CF(t):
    """Interest earned on net cashflows:
        valuation basis"""

    if t <= 0:
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        i = ((1 + Input.res_IR["Reserve IR"]) ** (1/12) - 1)
        return (Proj.DUR_M(t) <= Proj.POL_TERM_M()) * i * (PREM_PAYBL_M(t)
                                           - EXPS_ACQ(t)
                                           - EXPS_MAINT(t)
                                           - COMM(t)
                                           - INCM_BEN(t))


def DISC_RATE_M(t):
    """Monthly discount rate:
        valuation basis"""

    return (1 + Input.res_IR["Reserve IR"])**(1/12) - 1


def RESERVE(t):
    """Reserve calculation

    Reserve value at the period ``t`` is defined as::

        (reserve(t+1) - net_cf(t+1)) / (1 + disc_rate_mth())"""
    if t < 0:
        raise ValueError("t cannot be less than 0.")
    elif t >= Proj.PROJ_LEN().max():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return (Proj.DUR_M(t) < Proj.POL_TERM_M()) * (RESERVE(t+1) - NET_CF(t+1)) / (1 + DISC_RATE_M(t))


def RESERVE_PP(t):
    """Reserve value per policy
    Reserve value per policy at the period ``t`` is defined as::

        reserve(t) / pols_if(t)"""

    res = Input.np.array([RESERVE(t)], dtype = float)
    pols = Input.np.array([POLS_IF(t)], dtype = float)
    res_pp = Input.np.divide(res, pols, out = Input.np.zeros_like(res), where = pols!= 0)

    return Input.pd.Series(sum(res_pp), index = Proj.MP().index)


def INCM_BEN(t):
    """Expected income benefit:
        valuation basis"""
    if t <= 0:
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return Proj.INCM_FAC(t) * Proj.PREM_PP()/12 * POLS_IF(t-1)


# ---------------------------------------------------------------------------
# References

Proj = ("Interface", ("..", "Projection"), "auto")

Input = ("Interface", ("..", "Input"), "auto")