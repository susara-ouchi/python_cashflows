from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def DECLRD_REV_BONUS(t):

    """Declared Reversionary Bonus"""

    if t < 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index) 
    elif t == 0:
        return Input.DECLRD_BONUS()
    else:
        #Condition to check if date is bonus declaration date
        Flag = (Input.ValDate["Valuation Date"].month + t - Input.bonus_declr_mth["Month"]) % 12 == 0

        return (Proj.SUM_ASSURED() * Input.RevBonus_rt["Bonus Rate"] * Flag + DECLRD_REV_BONUS(t-1)) * Proj.IND_ACTIVE(t)


def RES_DECLRD_REV_BONUS(t):

    """Declared Reversionary Bonus:
        reserving"""

    if t < 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    elif t == 0:
        return Input.DECLRD_BONUS()
    else:
        #Condition to check if date is bonus declaration date
        Flag = (Input.ValDate["Valuation Date"].month + t - Input.bonus_declr_mth["Month"]) % 12 == 0

        return (Proj.SUM_ASSURED() * Input.res_RevBonus_rt["Reversionary"] * Flag + RES_DECLRD_REV_BONUS(t-1)) * Proj.IND_ACTIVE(t)


def COB_FAC_PP(t):

    """Cost of bonus factor per policy - reserving"""

    if t <= 0 or t > Proj.PROJ_LEN().max():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        Flag1 = Proj.DUR_M(t) == Proj.POL_TERM_M()
        Flag2 = Proj.DUR_M(t) < Proj.POL_TERM_M() 
        Surv_Fac = COB_FAC_PP(t + 1) * (1 - Res.MORT_RATE_MLY(t + 1))
        Death_Fac = Res.MORT_RATE_MLY(t + 1)
        Fac1 = (1 + Input.res_IR["Reserve IR"] - Input.res_inv_exp_pc["Investment Expenses %"])
        return Flag1 + (1 - Flag1) * Flag2 * (Surv_Fac / (Fac1 ** (1/12)) + Death_Fac / (Fac1 ** (1/24)))


def RES_COB_PP(t):

    """Cost of bonus value for reserving"""

    if t <= 0:
        return Input.pd.Series(0, index = Proj.MP().index)
    elif t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(1, index = Proj.MP().index)
    else:
        Flag = Proj.DUR_M(t) < Proj.POL_TERM_M()
        return Flag * COB_FAC_PP(t) * (RES_DECLRD_REV_BONUS(t+1) - RES_DECLRD_REV_BONUS(t))


def COB_PP(t):

    """Cost of bonus value for realisitic basis/BE"""

    if t <= 0:
        return Input.pd.Series(0, index = Proj.MP().index)
    elif t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(1, index = Proj.MP().index)
    else:
        Flag = Proj.DUR_M(t) < Proj.POL_TERM_M()
        return Flag * COB_FAC_PP(t) * (DECLRD_REV_BONUS(t+1) - DECLRD_REV_BONUS(t))


# ---------------------------------------------------------------------------
# References

Proj = ("Interface", ("..", "Projection"), "auto")

Input = ("Interface", ("..", "Input"), "auto")

Res = ("Interface", ("..", "Reserves"), "auto")