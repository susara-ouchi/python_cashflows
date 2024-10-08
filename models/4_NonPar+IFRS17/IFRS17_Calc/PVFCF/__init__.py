from modelx.serialize.jsonvalues import *

_formula = lambda CF, disc_rate, basis: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def PV_PREM(t):
    """Present value of premium payable"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = CF.COHORT().index)
    else:
        return CF.PREM_PAYBL_M(t) + PV_PREM(t+1)/(1 + disc_rate(t, basis))


def PV_DTH_BEN(t):
    """Present value of death benefits"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = CF.COHORT().index)
    else:
        return (CF.DTH_BEN(t) + PV_DTH_BEN(t+1)) / (1 + disc_rate(t, basis))


def PV_OTH_BEN(t):
    """Present value of surrender, income and 
    maturity benefits"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = CF.COHORT().index)
    else:
        return CF.INCM_BEN(t) + CF.MAT_BEN(t) + (CF.SURR_BEN(t) + PV_OTH_BEN(t+1))/(1 + disc_rate(t, basis))


def PV_COMM(t):
    """Present value of commission"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = CF.COHORT().index)
    else:
        return CF.COMM_INIT(t) + CF.COMM_REN(t) + PV_COMM(t+1)/(1 + disc_rate(t, basis))


def PV_EXPS(t):
    """Present value of maintenance and claim expenses"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = CF.COHORT().index)
    else:
        disc_fac = 1 + disc_rate(t, basis)
        return (CF.EXPS_MAINT(t) + CF.EXPS_CLAIM_MAT(t)
                + (CF.EXPS_CLAIM_DTH(t) + CF.EXPS_CLAIM_SURR(t) + PV_EXPS(t+1))/disc_fac)


def PV_EXPS_ACQ(t):
    """Present value of aquisition expenses"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = CF.COHORT().index)
    else:
        return CF.EXPS_ACQ(t) + PV_EXPS_ACQ(t+1)/(1 + disc_rate(t, basis))


def PV_RA_CF(t):
    """Present value of all risk adjusment cashflows"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = CF.COHORT().index)
    else:
        return (CF.RA_MORT(t) + PV_RA_CF(t+1)) / (1 + disc_rate(t, basis))


def BEL(t):
    """Best estimated liabilities at valuation"""

    if t < 0:
        return Input.pd.Series(0, index = CF.COHORT().index)
    else:
        Output.COHORT_CF()
        return -(PV_PREM(t+1)
                 - PV_DTH_BEN(t+1)
                 - PV_OTH_BEN(t+1)
                 - PV_EXPS_ACQ(t+1)
                 - PV_EXPS(t+1)
                 - PV_COMM(t+1))


def RA(t):
    """Risk adjustment at valuation"""

    if t < 0:
        return Input.pd.Series(0, index = CF.COHORT().index)
    else:
        Output.COHORT_CF()
        return PV_RA_CF(t+1)


def CSM(t):
    """Contractual Service Margin at valuation"""

    return Input.np.maximum(0, - BEL(t) - RA(t))


def LIAB(t):
    """Total Liability at initial recognisation"""

    return BEL(t) + RA(t) + CSM(t)


# ---------------------------------------------------------------------------
# References

Proj = ("Interface", ("...", "PolicyProjection"), "auto")

Input = ("Interface", ("...", "Input"), "auto")

Output = ("Interface", ("...", "Output"), "auto")