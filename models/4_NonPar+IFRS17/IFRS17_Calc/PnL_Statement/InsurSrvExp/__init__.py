from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def EST_LOSS(t):
    """Establishment of Loss Component"""

    if t < 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        return -RF.S_CSM.PVFCF(t)


def LOSS_RVRSL(t):
    """Reversal of Loss Component"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        return -RF.S_CSM.RELEASE(t)


def INS_OUT(t):
    """Actual Outflow: Insurance Component"""

    if t < 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        n, flag = Input.MAX_SCEN(), (t <= Rebased.VAL_M())

        return -((Act.INS_AFT_PROB(t)
                  + Act.EXPS_CLAIM_DTH(t)
                  + Act.EXPS_CLAIM_SURR(t)
                  + Act.EXPS_CLAIM_MAT(t)
                  + Act.EXPS_MAINT(t)
                  + Act.COMM_INIT(t)
                  + Act.COMM_REN(t)) * flag

                 + (Rebased(n).INS_AFT_PROB(t)
                   + Rebased(n).EXPS_CLAIM_DTH(t)
                   + Rebased(n).EXPS_CLAIM_SURR(t)
                   + Rebased(n).EXPS_CLAIM_MAT(t)
                   + Rebased(n).EXPS_MAINT(t)
                   + Rebased(n).COMM_INIT(t)
                   + Rebased(n).COMM_REN(t)) * (1 - flag))


def ACQ_CF_AMORT(t):
    """Amortization of Acquistion Cashflows"""

    if t < 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        return RF.AcqExpAmort.AMORT_EXP(t)


def INSUR_SRV_EXP(t):
    """Insurance Service Expense"""

    if t < 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        total = Input.pd.Series(0, index = BE.COHORT().index)
        Vars = list(INSUR_SRV_EXP.parent.cells); Vars.remove("INSUR_SRV_EXP")

        ## runs a loop to sum all variables except itself
        for cell in Vars:
            exec(f"total += {cell}(t)")

        return total


def S_CSM_XP_VAR(t):
    "Shadow CSM Experience Adjustment"

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        return - S_CSM.RELEASE_PREM(t) - S_CSM.RELEASE_INV(t) - S_CSM.XP_VAR(t)


def S_CSM_ASSM_CHG_ADJ(t):
    """Shadow CSM: Adjustment due to assumption changes

        assm: Inflation, Mortality
    """

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        return - (S_CSM.ASSM_CHG_LR(t, "Inflation")
                  + S_CSM.ASSM_CHG_LR(t, "Mortality"))


# ---------------------------------------------------------------------------
# References

Input = ("Interface", ("....", "Input"), "auto")

Act = ("Interface", ("...", "Actuals"), "auto")

BE = ("Interface", ("...", "BestEstimate"), "auto")

RF = ("Interface", ("...", "RollForward"), "auto")

S_CSM = ("Interface", ("...", "RollForward", "S_CSM"), "auto")

Rebased = ("Interface", ("...", "BestEstimateRebased"), "auto")