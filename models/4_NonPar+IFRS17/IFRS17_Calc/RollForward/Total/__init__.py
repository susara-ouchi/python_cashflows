from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def OPENING(t):
    """Opening value of Total Contract Liability"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        return BEL.OPENING(t) + RA.OPENING(t) + CSM.OPENING(t)


def PVFCF(t):
    """Present value of future cashflows"""

    if t < 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = CF.COHORT().index)
    else:
        return BEL.PVFCF(t) + RA.PVFCF(t) + CSM.PVFCF(t)


def EXPCT_IN(t):
    """Expected cash inflows"""

    if t < 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = CF.COHORT().index)
    else:
        return BEL.EXPCT_IN(t) + CSM.RELEASE_PREM(t)


def EXPCT_OUT(t):
    """Expected cash outflows"""

    if t < 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = CF.COHORT().index)
    else:
        return (BEL.EXPCT_INS_OUT(t) + BEL.EXPCT_INV_OUT(t) + CSM.RELEASE_INV(t))


def FIN_EFFECT(t):
    """Insurance finance expense"""

    if t < 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = CF.COHORT().index)
    else:
        return (BEL.FIN_EFFECT(t) +  RA.FIN_EFFECT(t) +  CSM.FIN_EFFECT(t))


def XP_VAR(t):
    """Adjustment to future cashflows due to -
        Experience variance
    """

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        return (BEL.XP_VAR_LR(t)
                + BEL.XP_VAR_CR(t)
                + RA.XP_VAR_LR(t)
                + RA.XP_VAR_CR(t)
                + CSM.XP_VAR_LR(t))


def ASSM_CHG_DISC(t):
    """Adjustment to future cashflows due to -
        Assumption change: discount rates
    """

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        return (BEL.ASSM_CHG_DISC(t)
                + RA.ASSM_CHG_DISC(t))


def ASSM_CHG(t, assm):
    """Adjustment to future cashflows due to -
        Assumption change:-

        assm: Inflation, Mortality"""

    if t <= 0 or t > Input.MAX_PROJ_LEN() or not(Input.ASSM_CHG_RUN(assm)):
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        return (BEL.ASSM_CHG_LR(t, assm)
                + BEL.ASSM_CHG_CR(t, assm)

                + RA.ASSM_CHG_LR(t, assm)
                + RA.ASSM_CHG_CR(t, assm)

                + CSM.ASSM_CHG_LR(t, assm))


def RELEASE(t):
    """Total release"""

    if t < 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = CF.COHORT().index)
    else:
        return RA.RELEASE(t) + CSM.RELEASE(t)


def CLOSING(t):
    """Closing value of Total Contract Liability"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        return (BEL.CLOSING(t) + RA.CLOSING(t) + CSM.CLOSING(t))


# ---------------------------------------------------------------------------
# References

Input = ("Interface", ("....", "Input"), "auto")

Proj = ("Interface", ("....", "PolicyProjection"), "auto")

BE = ("Interface", ("...", "BestEstimate"), "auto")

BEL = ("Interface", ("..", "BEL"), "auto")

RA = ("Interface", ("..", "RA"), "auto")

CSM = ("Interface", ("..", "CSM"), "auto")

S_CSM = ("Interface", ("..", "S_CSM"), "auto")