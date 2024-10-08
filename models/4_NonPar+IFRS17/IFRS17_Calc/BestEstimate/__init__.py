from modelx.serialize.jsonvalues import *

_formula = lambda : None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def COHORT():
    """Cohorts definition"""

    ## x = BestEstimate.COHORT().copy()
    ## x.index = BestEstimate.COHORT()

    x = Input.MP()["PCODE"].copy()
    x.index = Input.MP()["PCODE"]
    return x.groupby(x.index).count()


def COHORT_VAR(cell: str, *args):
    """Returns aggregated variables - cohortwise"""

    COHORT = Input.MP()["PCODE"]
    cellStr = "PolProj.BestEstimate."+cell

    def CohortSum(x: Input.pd.Series):
        var = x.copy()
        var.index = COHORT
        return var.groupby(var.index).sum()

    temp = CohortSum(Input.pd.Series(eval(f"{cellStr}{args[0]}")))
    return temp


def COMM_INIT(t):
    "Aggregated initial commission - cohortwise"

    return COHORT_VAR("COMM_INIT", t).rename("COMM_INIT")


def COMM_REN(t):
    "Aggregated renewal commission - cohortwise"

    return COHORT_VAR("COMM_REN", t).rename("COMM_REN")


def DTH_BEN(t):
    "Aggregated death benefit payouts - cohortwise"

    return COHORT_VAR("DTH_BEN", t).rename("DTH_BEN")


def EXPS(t):
    "Aggregated total expenses - cohortwise"

    return COHORT_VAR("EXPS", t).rename("EXPS")


def EXPS_ACQ(t):
    "Aggregated acquisition expenses - cohortwise"

    return COHORT_VAR("EXPS_ACQ", t).rename("EXPS_ACQ")


def EXPS_CLAIM_DTH(t):
    "Aggregated death claim expenses - cohortwise"

    return COHORT_VAR("EXPS_CLAIM_DTH", t).rename("EXPS_CLAIM_DTH")


def EXPS_CLAIM_MAT(t):
    "Aggregated maturity claim expenses - cohortwise"

    return COHORT_VAR("EXPS_CLAIM_MAT", t).rename("EXPS_CLAIM_MAT")


def EXPS_CLAIM_SURR(t):
    "Aggregated surrender claim expenses - cohortwise"

    return COHORT_VAR("EXPS_CLAIM_SURR", t).rename("EXPS_CLAIM_SURR")


def EXPS_MAINT(t):
    "Aggregated maintenance expenses - cohortwise"

    return COHORT_VAR("EXPS_MAINT", t).rename("EXPS_MAINT")


def INCM_BEN(t):
    "Aggregated income benefit payouts - cohortwise"

    return COHORT_VAR("INCM_BEN", t).rename("INCM_BEN")


def INS_AFT_PROB(t):
    """Insurance component after probability - cohortwise"""

    return COHORT_VAR("INS_AFT_PROB", t).rename("INS_AFT_PROB")


def INV_AFT_PROB(t):
    """Investment component after probability - cohortwise"""

    return COHORT_VAR("INV_AFT_PROB", t).rename("INV_AFT_PROB")


def MAT_BEN(t):
    "Aggregated maturity benefit payouts - cohortwise"

    return COHORT_VAR("MAT_BEN", t).rename("MAT_BEN")


def NET_CF(t):
    "Aggregated net cashflows - cohortwise"

    return COHORT_VAR("NET_CF", t).rename("NET_CF")


def POLS_IF(t):
    "Aggregated Policy inforce - cohortwise"

    return COHORT_VAR("POLS_IF", t).rename("POLS_IF")


def PREM_PAYBL_M(t):
    "Aggregated monthly premiums payable - cohortwise"

    return COHORT_VAR("PREM_PAYBL_M", t).rename("PREM_PAYBL_M")


def RA_MORT(t):
    """Risk adjustment: mortality"""

    if t == 0:
        return DTH_BEN(t) * 0
    else:
        y = Input.math.ceil((t+1)/12)
        return DTH_BEN(t) * Input.RiskAdjustment["Mortality"][y]


def SURR_BEN(t):
    "Aggregated surrender benefit payouts - cohortwise"

    return COHORT_VAR("SURR_BEN", t).rename("SURR_BEN")


# ---------------------------------------------------------------------------
# References

Input = ("Interface", ("...", "Input"), "auto")

PolProj = ("Interface", ("...", "PolicyProjection"), "auto")