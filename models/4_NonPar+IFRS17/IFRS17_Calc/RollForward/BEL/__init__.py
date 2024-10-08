from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def OPENING(t):
    """Opening value of BEL"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        return CLOSING(t-1)


def PVFCF(t):
    """Present value of future cashflows
    Can also be considered as opening due to new business."""

    if t != 1:
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        return PV(BE, Input.DISC_RATE_M, "Locked").BEL(t-1)


def EXPCT_IN(t):
    """Expected cash inflows"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        n, flag = Input.MAX_SCEN(), (t <= Rebased.VAL_M())
        return (flag * BE.PREM_PAYBL_M(t)
                + (1 - flag) * Rebased(n).PREM_PAYBL_M(t))


def EXPCT_INS_OUT(t):
    """Expected cash outflows: insurance component"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        n, flag = Input.MAX_SCEN(), (t <= Rebased.VAL_M())
        return (-(BE.EXPS_ACQ(t)
                  + BE.EXPS_MAINT(t)
                  + BE.EXPS_CLAIM_DTH(t)
                  + BE.EXPS_CLAIM_SURR(t)
                  + BE.COMM_INIT(t)
                  + BE.COMM_REN(t)
                  + BE.INS_AFT_PROB(t)) * flag

                -(Rebased(n).EXPS_ACQ(t)
                  + Rebased(n).EXPS_MAINT(t)
                  + Rebased(n).EXPS_CLAIM_DTH(t)
                  + Rebased(n).EXPS_CLAIM_SURR(t)
                  + Rebased(n).COMM_INIT(t)
                  + Rebased(n).COMM_REN(t)
                  + Rebased(n).INS_AFT_PROB(t)) * (1 - flag))


def EXPCT_INV_OUT(t):
    """Expected cash outflows: investment component"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        n, flag = Input.MAX_SCEN(), (t <= Rebased.VAL_M())
        return (flag * (- BE.INV_AFT_PROB(t) - BE.EXPS_CLAIM_MAT(t))
                + (1 - flag) * (- Rebased(n).INV_AFT_PROB(t) - Rebased(n).EXPS_CLAIM_MAT(t)))


def FIN_EFFECT(t):
    """Insurance finance expense"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        n, flag = Input.MAX_SCEN(), (t <= Rebased.VAL_M())
        best_est = (BE.PREM_PAYBL_M(t)
                    - BE.INCM_BEN(t)
                    - BE.MAT_BEN(t)
                    - BE.EXPS_ACQ(t)
                    - BE.EXPS_MAINT(t)
                    - BE.EXPS_CLAIM_MAT(t)
                    - BE.COMM_INIT(t)
                    - BE.COMM_REN(t))

        rebased = (Rebased(n).PREM_PAYBL_M(t)
                   - Rebased(n).INCM_BEN(t)
                   - Rebased(n).MAT_BEN(t)
                   - Rebased(n).EXPS_ACQ(t)
                   - Rebased(n).EXPS_MAINT(t)
                   - Rebased(n).EXPS_CLAIM_MAT(t)
                   - Rebased(n).COMM_INIT(t)
                   - Rebased(n).COMM_REN(t))

        return (best_est * flag
                + rebased * (1 - flag)
                + OPENING(t)
                + PVFCF(t))* Input.DISC_RATE_M(t, "Current")


def XP_VAR_LR(t):
    """Adjustment to future cashflows due to -
        Experience variance

        This is defined as:
            Expected BEL at locked-in rates
            minus
            BEL using Actuals at locked-in rates

        Refer IFRS17 sections B96(b)
    """
    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        return Rebased.IND_FCF_CHG(t) * (PV(Act, Input.DISC_RATE_M, "Locked").BEL(t)
                                        - PV(BE, Input.DISC_RATE_M, "Locked").BEL(t))


def XP_VAR_CR(t):
    """Adjustment to future cashflows due to -
        Experience variance

        This is defined as:
            BEL using Actuals at previous rates
            minus
            BEL using Actuals at locked-in rates

        Refer IFRS17 sections B96(b)
    """
    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        return Rebased.IND_FCF_CHG(t) * (PV(Act, Input.DISC_RATE_M, "Previous").BEL(t)
                                        - PV(Act, Input.DISC_RATE_M, "Locked").BEL(t))


def ASSM_CHG_DISC(t):
    """Adjustment to future cashflows due to -
        Assumption Change: Discount Rate

        Change in FCF from previous to current discount rate

        This is defined as:
            BEL using Actuals at current rates
            minus
            BEL using Actuals at previous rates

        Refer IFRS17 section B97(a)
    """
    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        return Rebased.IND_FCF_CHG(t) * (PV(Act, Input.DISC_RATE_M, "Current").BEL(t)
                                        - PV(Act, Input.DISC_RATE_M, "Previous").BEL(t))


def ASSM_CHG_LR(t, assm):
    """Adjustment to future cashflows due to -
        Assumption change: Inflation rate

        Change in FCF due to assumption changes at LR

        This is defined as:
            BEL using Rebased CFs at locked-in rates
            minus
            BEL using Actuals at locked-in rates

        Refer IFRS17 section B128(b)

        assm: Inflation, Mortality"""

    if t <= 0 or t > Input.MAX_PROJ_LEN() or not(Input.ASSM_CHG_RUN(assm)):
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        n = Input.ASSM_CHG_RUN(assm)
        return Rebased.IND_FCF_CHG(t) * (PV(Rebased(n), Input.DISC_RATE_M, "Locked").BEL(t)
                                        - PV(Rebased(n-1), Input.DISC_RATE_M, "Locked").BEL(t))


def ASSM_CHG_CR(t, assm):
    """Adjustment to future cashflows due to -
        Assumption change: Inflation rate

        Difference in change in FCF from assumption change between LR and CR

        This is defined as:
            Change in BEL between Rebased and Actuals at CR
            minus
            Change in BEL between Rebased and Actuals at LR

        Refer IFRS17 section B128(b)

        assm: Inflation, Mortality"""

    if t <= 0 or t > Input.MAX_PROJ_LEN() or not(Input.ASSM_CHG_RUN(assm)):
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        n = Input.ASSM_CHG_RUN(assm)
        return ((PV(Rebased(n), Input.DISC_RATE_M, "Current").BEL(t)
                 - PV(Rebased(n-1), Input.DISC_RATE_M, "Current").BEL(t))

               -(PV(Rebased(n), Input.DISC_RATE_M, "Locked").BEL(t)
                 - PV(Rebased(n-1), Input.DISC_RATE_M, "Locked").BEL(t))) * Rebased.IND_FCF_CHG(t)


def CLOSING(t):
    """Closing value of BEL"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        total = Input.pd.Series(0, index = BE.COHORT().index)
        Vars = list(CLOSING.parent.cells); Vars.remove("CLOSING")

        ## runs a loop to sum all variables except itself
        for cell in Vars:
            if eval(f"{cell}.parameters == ('t',)"):
                exec(f"total += {cell}(t)")
            elif eval(f"{cell}.parameters == ('t','assm')"): ## adds parameterized variables
                for arg in list(Input.AssumptionsMatrix.columns):
                    exec(f"total += {cell}(t, arg)")
        return total


# ---------------------------------------------------------------------------
# References

Input = ("Interface", ("....", "Input"), "auto")

BE = ("Interface", ("...", "BestEstimate"), "auto")

Act = ("Interface", ("...", "Actuals"), "auto")

Rebased = ("Interface", ("...", "BestEstimateRebased"), "auto")

PV = ("Interface", ("...", "PVFCF"), "auto")