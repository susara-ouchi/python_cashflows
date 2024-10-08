from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def OPENING(t):
    """Opening value of RA"""

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
        return PV(BE, Input.DISC_RATE_M, "Locked").RA(t-1)


def FIN_EFFECT(t):
    """Insurance finance expense"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        return (OPENING(t) + PVFCF(t)) * Input.DISC_RATE_M(t, "Current")


def XP_VAR_LR(t):
    """Adjustment to future Risk Adjustment due to -
        Experience variance

        This is defined as:
            RA using Actuals at previous rates
            minus
            Expected RA at locked-in rates

        Refer IFRS17 sections B96(d)      
    """
    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        return Rebased.IND_FCF_CHG(t) * (PV(Act, Input.DISC_RATE_M, "Locked").RA(t)
                                        - PV(BE, Input.DISC_RATE_M, "Locked").RA(t))


def XP_VAR_CR(t):
    """Adjustment to future Risk Adjustment due to -
        Experience variance

        This is defined as:
            RA using Actuals at current rates
            minus
            RA using Actuals at previous rates

        Refer IFRS17 sections B96(d)      
    """
    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        return Rebased.IND_FCF_CHG(t) * (PV(Act, Input.DISC_RATE_M, "Previous").RA(t)
                                        - PV(Act, Input.DISC_RATE_M, "Locked").RA(t))


def ASSM_CHG_DISC(t):
    """Adjustment to future cashflows due to -
        Assumption Change: Discount Rate

        Change in FCF from previous to current discount rate

        This is defined as:
            RA using Actuals at current rates
            minus
            RA using Actuals at previous rates

        Refer IFRS17 section B97(a)
    """
    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        return Rebased.IND_FCF_CHG(t) * (PV(Act, Input.DISC_RATE_M, "Current").RA(t)
                                        - PV(Act, Input.DISC_RATE_M, "Previous").RA(t))


def ASSM_CHG_LR(t, assm):
    """Adjustment to future cashflows due to -
        Assumption change: Inflation rate

        Change in FCF due to assumption changes at LR

        This is defined as:
            RA using Rebased CFs at locked-in rates
            minus
            RA using Actuals at locked-in rates

        Refer IFRS17 section B128(b)

        assm: Inflation, Mortality"""

    if t <= 0 or t > Input.MAX_PROJ_LEN() or not(Input.ASSM_CHG_RUN(assm)):
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        n = Input.ASSM_CHG_RUN(assm)
        return Rebased.IND_FCF_CHG(t) * (PV(Rebased(n), Input.DISC_RATE_M, "Locked").RA(t)
                                        - PV(Rebased(n-1), Input.DISC_RATE_M, "Locked").RA(t))


def ASSM_CHG_CR(t, assm):
    """Adjustment to future cashflows due to -
        Assumption change: Inflation rate

        Difference in change in RA from assumption change between LR and CR

        This is defined as:
            Change in RA between Rebased and Actuals at CR
            minus
            Change in RA between Rebased and Actuals at LR

        Refer IFRS17 section B128(b)

        assm: Inflation, Mortality"""

    if t <= 0 or t > Input.MAX_PROJ_LEN() or not(Input.ASSM_CHG_RUN(assm)):
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        n = Input.ASSM_CHG_RUN(assm)
        return ((PV(Rebased(n), Input.DISC_RATE_M, "Current").RA(t)
                 - PV(Rebased(n-1), Input.DISC_RATE_M, "Current").RA(t))

               -(PV(Rebased(n), Input.DISC_RATE_M, "Locked").RA(t)
                 - PV(Rebased(n-1), Input.DISC_RATE_M, "Locked").RA(t))) * Rebased.IND_FCF_CHG(t)


def RELEASE(t):
    """RA Release"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        n, flag = Input.MAX_SCEN(), (t <= Rebased.VAL_M())
        return - (flag * BE.RA_MORT(t) + (1 - flag) * Rebased(n).RA_MORT(t))


def CLOSING(t):
    """Closing value of RA"""

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

Proj = ("Interface", ("....", "PolicyProjection"), "auto")

BE = ("Interface", ("...", "BestEstimate"), "auto")

Act = ("Interface", ("...", "Actuals"), "auto")

Rebased = ("Interface", ("...", "BestEstimateRebased"), "auto")

PV = ("Interface", ("...", "PVFCF"), "auto")