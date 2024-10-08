from modelx.serialize.jsonvalues import *

_formula = lambda : None

_bases = []

_allow_none = None

_spaces = [
    "BEL",
    "RA",
    "CSM",
    "S_CSM",
    "Total",
    "AcqExpAmort",
    "Assets"
]

# ---------------------------------------------------------------------------
# Cells

def COV_UNIT(t):

    """Coverage units for CSM and Acquisition ammortization"""

    if t < 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = BE.COHORT().index)
    else:
        t_len = range(t, Input.MAX_PROJ_LEN())
        pols = BE.POLS_IF(t)
        sum_pols = sum([BE.POLS_IF(i) for i in t_len])
        cov = Input.np.divide(pols, sum_pols, out = Input.np.zeros_like(sum_pols), where = sum_pols!= 0)

        return cov


# ---------------------------------------------------------------------------
# References

Proj = ("Interface", ("...", "PolicyProjection"), "auto")

Input = ("Interface", ("...", "Input"), "auto")

BE = ("Interface", ("..", "BestEstimate"), "auto")