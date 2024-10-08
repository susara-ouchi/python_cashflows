from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def CSM_RELEASE(t):
    """Release of CSM"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        return -RF.CSM.RELEASE(t)


def LOSS_RELEASE(t):
    """Release of Loss Component"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        return RF.S_CSM.RELEASE(t)


def RA_RELEASE(t):
    """Release of Risk Adjustement"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        return -RF.RA.RELEASE(t)


def INS_OUT(t):
    """Expected Outflow - Insurance Component"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        n, flag = Input.MAX_SCEN(), (t <= Rebased.VAL_M())

        return ((BE.INS_AFT_PROB(t)
                + BE.EXPS_CLAIM_DTH(t)
                + BE.EXPS_CLAIM_SURR(t)
                + BE.EXPS_CLAIM_MAT(t)
                + BE.EXPS_MAINT(t)
                + BE.COMM_INIT(t)
                + BE.COMM_REN(t)) * flag

                + (Rebased(n).INS_AFT_PROB(t)
                   + Rebased(n).EXPS_CLAIM_DTH(t)
                   + Rebased(n).EXPS_CLAIM_SURR(t)
                   + Rebased(n).EXPS_CLAIM_MAT(t)
                   + Rebased(n).EXPS_MAINT(t)
                   + Rebased(n).COMM_INIT(t)
                   + Rebased(n).COMM_REN(t)) * (1 - flag))


def ACQ_CF_RECOVER(t):
    """Recovery of Acquisiton Cashflows"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        return -RF.AcqExpAmort.AMORT_EXP(t)


def INSUR_SRV_REV(t):
    """Insurance Service Revenue"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        total = Input.pd.Series(0, index = BE.COHORT().index)
        Vars = list(INSUR_SRV_REV.parent.cells); Vars.remove("INSUR_SRV_REV")

        ## runs a loop to sum all variables except itself
        for cell in Vars:
            exec(f"total += {cell}(t)")

        return total


# ---------------------------------------------------------------------------
# References

Input = ("Interface", ("....", "Input"), "auto")

Proj = ("Interface", ("....", "PolicyProjection"), "auto")

BE = ("Interface", ("...", "BestEstimate"), "auto")

RF = ("Interface", ("...", "RollForward"), "auto")

Rebased = ("Interface", ("...", "BestEstimateRebased"), "auto")