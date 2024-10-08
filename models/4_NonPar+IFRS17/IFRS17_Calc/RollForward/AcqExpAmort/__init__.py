from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def OPENING(t):
    """Opening value of Acq Expense"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        return CLOSING(t-1)


def NEW_ACQ_EXP(t):
    """New Acquisition Expense"""

    if t < 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        return BE.EXPS_ACQ(t)


def ACCR_INT(t):
    """Accretion of interest"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        return (OPENING(t) + NEW_ACQ_EXP(t)) * Input.DISC_RATE_M(t, "Current")


def AMORT_EXP(t):
    """Amortised Expense"""

    if t < 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        RFW = AMORT_EXP.parent.parent
        return -(OPENING(t) + NEW_ACQ_EXP(t) + ACCR_INT(t)) * RFW.COV_UNIT(t)


def CLOSING(t):
    """Closing value of Acquistion Expense"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        return (OPENING(t) + NEW_ACQ_EXP(t) + ACCR_INT(t) + AMORT_EXP(t))


# ---------------------------------------------------------------------------
# References

Input = ("Interface", ("....", "Input"), "auto")

Proj = ("Interface", ("....", "PolicyProjection"), "auto")

BE = ("Interface", ("...", "BestEstimate"), "auto")