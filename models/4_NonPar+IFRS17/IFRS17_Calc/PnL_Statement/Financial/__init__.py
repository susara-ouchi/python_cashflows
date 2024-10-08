from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def INV_INC(t):
    """Investment Income (Actual)"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        n, flag = Input.MAX_SCEN(), (t <= Rebased.VAL_M())

        actuals = (Act.PREM_PAYBL_M(t)
                   - Act.INCM_BEN(t)
                   - Act.MAT_BEN(t)
                   - Act.EXPS_ACQ(t)
                   - Act.EXPS_MAINT(t)
                   - Act.EXPS_CLAIM_MAT(t)
                   - Act.COMM_INIT(t)
                   - Act.COMM_REN(t))

        rebased = (Rebased(n).PREM_PAYBL_M(t)
                   - Rebased(n).INCM_BEN(t)
                   - Rebased(n).MAT_BEN(t)
                   - Rebased(n).EXPS_ACQ(t)
                   - Rebased(n).EXPS_MAINT(t)
                   - Rebased(n).EXPS_CLAIM_MAT(t)
                   - Rebased(n).COMM_INIT(t)
                   - Rebased(n).COMM_REN(t))

        return (RF.Total.OPENING(t)
                + actuals * flag
                + rebased * (1 - flag)) * Input.AST_EARN_RATE_M(t, "Current")


def INSUR_FIN_EXP(t):
    """Insurance Financial Expense"""

    if t < 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        return (-RF.BEL.XP_VAR_CR(t)
                -RF.BEL.ASSM_CHG_DISC(t)
                -RF.BEL.ASSM_CHG_CR(t, "Inflation")
                -RF.BEL.ASSM_CHG_CR(t, "Mortality")

                -RF.RA.ASSM_CHG_DISC(t)
                -RF.RA.ASSM_CHG_CR(t, "Inflation")
                -RF.RA.ASSM_CHG_CR(t, "Mortality")

                -RF.Total.FIN_EFFECT(t))


def FIN_PNL(t):
    """Financial Gain and Loss"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        return INV_INC(t) + INSUR_FIN_EXP(t)


# ---------------------------------------------------------------------------
# References

Input = ("Interface", ("....", "Input"), "auto")

Proj = ("Interface", ("....", "PolicyProjection"), "auto")

BE = ("Interface", ("...", "BestEstimate"), "auto")

Act = ("Interface", ("...", "Actuals"), "auto")

RF = ("Interface", ("...", "RollForward"), "auto")

Rebased = ("Interface", ("...", "BestEstimateRebased"), "auto")