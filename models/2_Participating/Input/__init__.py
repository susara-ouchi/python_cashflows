from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def DECLRD_BONUS():
    """Declared Reversionary Bonus as on the valuation date"""

    return Proj.MP()["declrd_bonus"]


def BASE_MORT_RATE(t):

    """Base mortality rates at time t"""

    if t <= 0:
        return pd.Series(0, index = Proj.MP().index)
    else:
        n = mort_table.index.max()
        ages = list(np.minimum(Proj.AGE(t-1), n)); mort_rates = 0

        for i in list(mort_table.columns):
            mort_rates += (Proj.SEX() == i) * list(mort_table[i][ages])
        return pd.Series(mort_rates, name = inspect.stack()[0][3])


def GSV_FAC(t):

    """Guaranteed Surrender Value Factors"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return pd.Series(0, index = Proj.MP().index)
    else:
        n = GSV_Factor.index.max()
        y = np.minimum((Proj.DUR_M(t)/12).apply(math.ceil), n)

        return ((Proj.POL_TERM_Y() == 10) * list(GSV_Factor["10Y Term"][y])
                + (Proj.POL_TERM_Y() == 15) * list(GSV_Factor["15Y Term"][y])
                + (Proj.POL_TERM_Y() == 20) * list(GSV_Factor["20Y Term"][y]))


def ACB_FAC(t):

    """Accrued Bonus Factors"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return pd.Series(0, index = Proj.MP().index)
    else:
        n = AccruedRates.index.max()
        y = np.minimum((Proj.DUR_M(t)/12).apply(math.ceil), n)

        return ((Proj.POL_TERM_Y() == 10) * list(AccruedRates["10Y Term"][y])
                + (Proj.POL_TERM_Y() == 15) * list(AccruedRates["15Y Term"][y])
                + (Proj.POL_TERM_Y() == 20) * list(AccruedRates["20Y Term"][y]))


def COHORT():

    """The cohort of the model points"""

    return Proj.MP()["pcode"]


# ---------------------------------------------------------------------------
# References

inspect = ("Module", "inspect")

pd = ("Module", "pandas")

np = ("Module", "numpy")

model_point_table = ("IOSpec", 2470946571936, 2470939166224)

exp_acq = ("IOSpec", 2470946579040, 2470946579040)

exp_claim = ("IOSpec", 2470952791744, 2470952791744)

exp_maint = ("IOSpec", 2470952061344, 2470952061344)

infl_rate = ("IOSpec", 2470952793088, 2470952793088)

mad = ("IOSpec", 2470946577744, 2470946577744)

mort_scale = ("IOSpec", 2470946576016, 2470946576016)

res_exp_acq = ("IOSpec", 2470952533152, 2470952533152)

res_exp_claim = ("IOSpec", 2470952533200, 2470952533200)

res_exp_maint = ("IOSpec", 2470952533344, 2470952533344)

res_infl_rate = ("IOSpec", 2470952531040, 2470952531040)

res_IR = ("IOSpec", 2470952531232, 2470952531232)

res_mort_scale = ("IOSpec", 2470952523312, 2470952523312)

SM_Rates = ("IOSpec", 2470952523840, 2470952523840)

Tax_Rates = ("IOSpec", 2470952523504, 2470952523504)

mat_fac = ("IOSpec", 2470952524176, 2470952524176)

model_path = ("IOSpec", 2470952523984, 2470952523984)

math = ("Module", "math")

SurrTerm = ("IOSpec", 2470952524608, 2470952524608)

GSV_Factor = ("IOSpec", 2470952864352, 2470953624352)

mort_table = ("IOSpec", 2470953680656, 2470953624592)

yield_curve = ("IOSpec", 2470952866272, 2470952524224)

lapse_table = ("IOSpec", 2470952864016, 2470952523888)

comm_rates = ("IOSpec", 2470953755712, 2470953679936)

RevBonus_rt = ("IOSpec", 2470952863632, 2470952863632)

AccruedRates = ("IOSpec", 2470954272128, 2470952866512)

sh_prop = ("IOSpec", 2470954272896, 2470954272896)

incm_ben_flag = ("IOSpec", 2470954285376, 2470954285376)

bonus_declr_mth = ("IOSpec", 2470954285520, 2470954285520)

ValDate = ("IOSpec", 2470954279856, 2470954279856)

res_RevBonus_rt = ("IOSpec", 2470954281392, 2470954281392)

res_terminal_bonus_rt = ("IOSpec", 2470954285712, 2470954285712)

surr_start_term = ("IOSpec", 2470954285616, 2470954285616)

res_inv_exp_pc = ("IOSpec", 2470954283504, 2470954283504)

inv_exp_pc = ("IOSpec", 2470954271504, 2470954271504)

term_bon_flag = ("IOSpec", 2470954285760, 2470954285760)

Proj = ("Interface", ("..", "Projection"), "auto")

point_id = 0