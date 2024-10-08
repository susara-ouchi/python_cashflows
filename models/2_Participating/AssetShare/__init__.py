from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def COMM(t):

    """Commissions:
        Best estimate"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        n = Input.comm_rates.index.max()
        dur_m = list(Input.np.minimum(Input.np.ceil(Proj.DUR_M(t)/12), n))
        comm_rates = Input.comm_rates["Projection"][dur_m]

        return Proj.IND_ACTIVE(t) * PREM_PAYBL_M(t) * list(comm_rates) * POLS_IF(t)


def DTH_BEN(t):

    """Death claims:
        Best estimate WO probability"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:    
        return Proj.IND_ACTIVE(t) * (Input.np.maximum(Input.np.maximum(Proj.SUM_ASSURED(), 10 * Proj.PREM_PP()), Proj.DUR_M(t) * 1.05 * (Proj.PREM_PP() / 12))
                                     + cob.DECLRD_REV_BONUS(t))


def EXPS(t):

    """Total expenses:
        Best estimate

        Accounting for acquisition, maintenance
        and claim expenses
    """

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        acq   = EXPS_ACQ(t) * (Proj.DUR_M(t-1) == 0)
        maint = EXPS_MAINT(t)
        claim = EXPS_CLAIM(t) 
        return Proj.IND_ACTIVE(t) * (acq + maint + claim)


def EXPS_ACQ(t):

    """Acquisition expense per policy:
        Best estimate WO probability"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        i        = Input.exp_acq["Fixed"]
        per_prem = Input.exp_acq["% of Premium"]
        per_sa   = Input.exp_acq["% of SA"]

        exp_acq = i + per_prem * Proj.PREM_PP() + per_sa * Proj.SUM_ASSURED()
        return exp_acq * (Proj.DUR_M(t-1) == 0) * POLS_IF(t)


def EXPS_CLAIM(t):

    """Expenses incured at death/surrender/maturity:
        Best estimate WO prob"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return Proj.IND_ACTIVE(t) * Input.exp_claim["Claims"] * Proj.INFL_FAC(t)*POLS_IF(t)


def EXPS_MAINT(t):

    """Annual maintenance expense per policy:
        Best estimate WO probability"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        e           = Input.exp_maint["Fixed"]/12 * Proj.INFL_FAC(t)
        per_prem    = Input.exp_maint["% of Premium"]
        per_res     = 1 - (1 - Input.exp_maint["% of Reserve"]) ** (1/12)
        flag        = (Proj.DUR_M(t-1) > 0) * (Proj.DUR_M(t) <= Proj.POL_TERM_M())

        return flag * ( e + per_prem * Proj.PREM_PP()/12+ per_res * Proj.RESERVE_PP(t-1))*POLS_IF(t)


def GROSS_TRNS_SH(t):

    """Gross Transfer to Shareholders WO probability"""

    sh = Input.sh_prop["Share"]
    tax_sh = Input.Tax_Rates["Shareholder"]
    return (cob.COB_PP(t)
            + TERMINAL_BON_MAT(t)) * sh / (1 - sh) / (1 - tax_sh)


def MAT_BEN(t):

    """Maturity benefit:
        Best estimate WO probability"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return (Proj.DUR_M(t) == Proj.POL_TERM_M() + 1) * (Proj.SUM_ASSURED() + cob.DECLRD_REV_BONUS(t-1)) * POLS_IF(t)


def TAX_SH_PH_TRNS(t):

    """Tax on SH and PH Transfer WO probability"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return (cob.COB_PP(t)
                + TERMINAL_BON_MAT(t)) * Input.Tax_Rates["Policyholder"] / (1-Input.Tax_Rates["Policyholder"])


def PREM_PAYBL_M(t):

    """Premium income - Asset Share calc"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return Proj.PREM_PP() / 12 * Proj.IND_ACTIVE(t)


def TERMINAL_BON_DTH(t):

    """Terminal Bonus Payable on Death - Assets Share"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return Input.np.maximum(AST_SHARE_BFR_EXT(t) - DTH_BEN(t) - EXPS_CLAIM(t), 0) * (1 - Input.Tax_Rates["Policyholder"]) * (1 - Input.sh_prop["Share"]) * Proj.IND_ACTIVE(t)


def TERMINAL_BON_MAT(t):

    """Terminal Bonus Payable on Maturity - Assets Share"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return (Proj.DUR_M(t) == Proj.POL_TERM_M() + 1) * Input.np.maximum(AST_SHARE_START(t) - MAT_BEN(t) - EXPS_CLAIM(t), 0) * (1 - Input.Tax_Rates["Policyholder"]) * (1 - Input.sh_prop["Share"])


def MORT_RISK_CHG(t): 

    """Mortality risk charge
        Best estimate"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return Proj.IND_ACTIVE(t) * Input.np.maximum(DTH_BEN(t) + EXPS_CLAIM(t) - AST_SHARE_BFR_EXT(t), 0) * Proj.MORT_RATE_MLY(t) / (1 - Proj.MORT_RATE_MLY(t))


def AST_SHARE_START(t):

    """Asset share at starting of month ``t``"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return (Proj.DUR_M(t) <= Proj.POL_TERM_M() + 1) * AST_SHARE_END(t-1)


def AST_SHARE_END(t):

    """Asset share at end of month ``t``"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return (AST_SHARE_BFR_EXT(t)
                - MORT_RISK_CHG(t)
                - GROSS_TRNS_SH(t)
                - TAX_SH_PH_TRNS(t))


def AST_SHARE_BFR_EXT(t):

    """Asset share before exit at month ``t``"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return (AST_SHARE_START(t)
                + PREM_PAYBL_M(t)
                + INT_AST_SHARE(t)
                - COMM(t)
                - EXPS_ACQ(t)
                - EXPS_MAINT(t)
                - MAT_BEN(t)
                - TERMINAL_BON_MAT(t))


def INT_AST_SHARE(t):

    """Interest on Asset share"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        y = Input.math.ceil(t/12)
        i = (1 + Input.yield_curve["Interest Rates"][y]) ** (1/12) - 1
        return (AST_SHARE_START(t)
                + PREM_PAYBL_M(t)
                - MAT_BEN(t-1)
                - COMM(t)
                - EXPS_ACQ(t)
                - EXPS_MAINT(t)) * i * Proj.IND_ACTIVE(t)


def POLS_IF(t):

    """Number of policies in-force
    For Asset share- it is hardcoded to 1"""

    if t < 0:
        raise ValueError("t cannot be less than 0.")
    elif t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return Input.pd.Series(1, index = Proj.MP().index)


# ---------------------------------------------------------------------------
# References

Proj = ("Interface", ("..", "Projection"), "auto")

Input = ("Interface", ("..", "Input"), "auto")

cob = ("Interface", ("..", "COBFactor"), "auto")