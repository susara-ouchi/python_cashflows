from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def OPENING(t):
    """Opening value of CSM"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        return CLOSING(t-1)


def PVFCF(t):
    """Present value of future cashflows"""

    if t != 1:
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        ind = (PV(BE, Input.DISC_RATE_M, "Locked").CSM(0) > 0)
        return ind * PV(BE, Input.DISC_RATE_M, "Locked").CSM(t-1)


def RELEASE_PREM(t):
    """
    Release of premium

    Defined as: If Init_CSM(0) > 0, Act.PREM - Rebased.PREM 

    The premiums beyond valuations are projected in Rebased spaces.
    However, future expected premiums are assumed to be equal to actuals,
    hence there is no componet for (t > Rebased.VAL_M())
    """

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        ind = (PV(BE, Input.DISC_RATE_M, "Locked").CSM(0) > 0)
        n, flag = Input.MAX_SCEN(), (t <= Rebased.VAL_M())

        return ind * flag * (Act.PREM_PAYBL_M(t) - BE.PREM_PAYBL_M(t))


def RELEASE_INV(t):
    """
    Release of Investment Component and Acquisition Costs

    The investment component beyond valuations are projected in Rebased spaces.
    However, future expected investment components are assumed to be equal to actuals,
    hence there is no componet for (t > Rebased.VAL_M())
    """

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        ind = (PV(BE, Input.DISC_RATE_M, "Locked").CSM(0) > 0)
        n, flag = Input.MAX_SCEN(), (t <= Rebased.VAL_M())

        return ind * flag * (BE.INV_AFT_PROB(t)
                             + BE.EXPS_ACQ(t)
                             + BE.COMM_INIT(t)

                               - Act.INV_AFT_PROB(t)
                               - Act.EXPS_ACQ(t)
                               - Act.COMM_INIT(t))


def FIN_EFFECT(t):
    """Insurance finance expense"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        return (OPENING(t) + PVFCF(t)) * Input.DISC_RATE_M(t, "Locked")


def XP_VAR_LR(t):
    """Adjustment to future Risk Adjustment due to -
        Experience variance

        This is defined as:
            CSM using Actuals at locked in rates
            minus
            Expected CSM at locked in rates

        Also reconciles with BEL.XP_VAR_LR(t) + RA.XP_VAR_LR(t)
    """

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        ind = Rebased.IND_FCF_CHG(t) * (PV(BE, Input.DISC_RATE_M, "Locked").CSM(0) > 0)
        return ind * (PV(Act, Input.DISC_RATE_M, "Locked").CSM(t)
                      - PV(BE, Input.DISC_RATE_M, "Locked").CSM(t))


def ASSM_CHG_LR(t, assm):
    """Adjustment to future cashflows due to -
        Assumption change: Inflation rate

        Change in FCF due to assumption changes at LR

        This is defined as:
            CSM using Rebased CFs at locked-in rates
            minus
            CSM using Actuals at locked-in rates

        Refer IFRS17 section B128(b)

        assm: Inflation, Mortality"""

    if t <= 0 or t > Input.MAX_PROJ_LEN() or not(Input.ASSM_CHG_RUN(assm)):
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        n = Input.ASSM_CHG_RUN(assm)
        ind = Rebased.IND_FCF_CHG(t) * (PV(BE, Input.DISC_RATE_M, "Locked").CSM(0) > 0)
        return ind * (PV(Rebased(n), Input.DISC_RATE_M, "Locked").CSM(t)
                      - PV(Rebased(n-1), Input.DISC_RATE_M, "Locked").CSM(t))


def RELEASE(t):
    """CSM Release"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        ind = (PV(BE, Input.DISC_RATE_M, "Locked").CSM(0) > 0)
        RFW = RELEASE.parent.parent
        total = Input.pd.Series(0, index = BE.COHORT().index)
        Vars = list(CLOSING.parent.cells)
        Vars.remove("RELEASE"); Vars.remove("CLOSING")

        ## runs a loop to sum all variables except itself and CLOSING
        for cell in Vars:
            if eval(f"{cell}.parameters == ('t',)"):
                exec(f"total += {cell}(t)")
            elif eval(f"{cell}.parameters == ('t','assm')"): ## adds parameterized variables
                for arg in list(Input.AssumptionsMatrix.columns):
                    exec(f"total += {cell}(t, arg)")

        return - (ind * total * RFW.COV_UNIT(t))


def CLOSING(t):
    """Closing value of CSM"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        ind = (PV(BE, Input.DISC_RATE_M, "Locked").CSM(0) > 0)
        total = Input.pd.Series(0, index = BE.COHORT().index)
        Vars = list(CLOSING.parent.cells); Vars.remove("CLOSING")

        ## runs a loop to sum all variables except itself
        for cell in Vars:
            if eval(f"{cell}.parameters == ('t',)"):
                exec(f"total += {cell}(t)")
            elif eval(f"{cell}.parameters == ('t','assm')"): ## adds parameterized variables
                for arg in list(Input.AssumptionsMatrix.columns):
                    exec(f"total += {cell}(t, arg)")

        return ind * total


# ---------------------------------------------------------------------------
# References

Input = ("Interface", ("....", "Input"), "auto")

BE = ("Interface", ("...", "BestEstimate"), "auto")

Act = ("Interface", ("...", "Actuals"), "auto")

Rebased = ("Interface", ("...", "BestEstimateRebased"), "auto")

PV = ("Interface", ("...", "PVFCF"), "auto")