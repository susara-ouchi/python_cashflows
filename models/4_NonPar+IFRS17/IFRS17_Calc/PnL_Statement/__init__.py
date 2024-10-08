from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = [
    "InsurSrvRev",
    "InsurSrvExp",
    "Financial"
]

# ---------------------------------------------------------------------------
# Cells

def PNL(t):
    """Profit and Loss"""

    if t < 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        return (InsurSrvRev.INSUR_SRV_REV(t)
                + InsurSrvExp.INSUR_SRV_EXP(t)
                + Financial.FIN_PNL(t))


# ---------------------------------------------------------------------------
# References

Proj = ("Interface", ("...", "PolicyProjection"), "auto")

Input = ("Interface", ("...", "Input"), "auto")

BE = ("Interface", ("..", "BestEstimate"), "auto")