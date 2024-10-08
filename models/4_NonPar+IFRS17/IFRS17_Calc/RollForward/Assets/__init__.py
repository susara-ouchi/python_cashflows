from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def OPENING(t):
    """Opening Assets"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        return CLOSING(t-1)


def CF(t):
    """Cashflows at Beginning of the month"""

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

        return (flag * actuals + (1 - flag) * rebased)


def INV_INC(t):
    """Investment Income"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        return (OPENING(t) + CF(t)) * Input.AST_EARN_RATE_M(t, "Current")


def BENEFITS(t):
    """Benefits at the End of the Month"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        n, flag = Input.MAX_SCEN(), (t <= Rebased.VAL_M())

        actual = -(Act.DTH_BEN(t)
                   + Act.SURR_BEN(t)
                   + Act.EXPS_CLAIM_DTH(t)
                   + Act.EXPS_CLAIM_SURR(t))

        rebased = -(Rebased(n).DTH_BEN(t)
                    + Rebased(n).SURR_BEN(t)
                    + Rebased(n).EXPS_CLAIM_DTH(t)
                    + Rebased(n).EXPS_CLAIM_SURR(t))

        return (flag * actual + (1 - flag) * rebased)


def PROFIT_RELEASE(t):
    """Release of Profit"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        return -PnL.PNL(t)


def CLOSING(t):
    """Closing Assets"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        return (OPENING(t)
                + CF(t)
                + INV_INC(t)
                + BENEFITS(t)
                + PROFIT_RELEASE(t))


# ---------------------------------------------------------------------------
# References

Input = ("Interface", ("....", "Input"), "auto")

Proj = ("Interface", ("....", "PolicyProjection"), "auto")

BE = ("Interface", ("...", "BestEstimate"), "auto")

Act = ("Interface", ("...", "Actuals"), "auto")

PnL = ("Interface", ("...", "PnL_Statement"), "auto")

Rebased = ("Interface", ("...", "BestEstimateRebased"), "auto")