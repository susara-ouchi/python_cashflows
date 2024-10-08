from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def ADMIN_CHARGE_RATE(t):
    """ Admin Charge"""

    if t <= 0:
        return pd.Series(0, index = Proj.MP().index)
    else:
        n = AdminCharge.index.max()
        dur = list(np.minimum(Proj.DUR_Y(t), n))
        return pd.Series(list(AdminCharge["Projection"][dur]), index = Proj.MP().index)


def BASE_MORT_RATE(t):
    """Base mortality rates at time t
    Base rates are common for projection and reserving"""

    ages = list(Proj.AGE(t-1)); sex = list(Mortality.columns)
    mort_rates = 0

    for i in sex:
        mort_rates += (Proj.SEX() == i) * list(Mortality[i][ages])

    return pd.Series(mort_rates, name = inspect.stack()[0][3])


def CHG_MORT_RATE(t):
    """Base mortality rates at time t"""\
    """Base rates are common for projection and reserving"""

    ages = list(Proj.AGE(t)); sex = list(ChargeMort.columns)
    chg_mort = 0

    for i in sex:
        chg_mort += (Proj.SEX() == i) * list(ChargeMort[i][ages])

    return pd.Series(chg_mort, name = inspect.stack()[0][3])


def SURR_CHG_RATE(t):
    """Surrender charge rates """

    if t <= 0:
        return pd.Series(0, index = Proj.MP().index)
    else:
        n = SurrCharge.index.max()
        dur = list(np.minimum(Proj.DUR_Y(t), n))
        surr_charge = ( np.array(SurrCharge["Premium<=25000"][dur])*(Proj.MP()["ann_prem"]<=25000) + 
                    np.array(SurrCharge["Premium>25000"][dur])*(Proj.MP()["ann_prem"]>25000) )
        return pd.Series(surr_charge, index = Proj.MP().index, name = "0")


def SURR_CHG_CAP(t):
    """Maximum surrender charge cap value """

    if t <= 0:
        return pd.Series(0, index = Proj.MP().index)
    else:
        n = SurrChargeCap.index.max()
        dur = list(np.minimum(Proj.DUR_Y(t), n))
        surr_cap = ( np.array(SurrChargeCap["Premium<=25000"][dur]) * (Proj.MP()["ann_prem"]<=25000)+  
                 np.array(SurrChargeCap["Premium>25000"][dur]) * (Proj.MP()["ann_prem"]>25000) )
        surr_cap.name = "0"
        return surr_cap


def LOYALTY_RATE(t):
    """Loyalty addition rates """

    if t <= 0:
        return pd.Series(0, Proj.MP().index)
    else:
        n = LoyaltyAdd.index.max()
        dur = list(np.minimum(Proj.DUR_Y(t), n))
        return pd.Series(list(LoyaltyAdd["Projection"][dur]), index = Proj.MP().index)


def CLAWBACK_RATE(t):
    """Clawback Rates"""


    dur = Proj.DUR_M(t).rename("Month")
    rate = pd.merge_asof(dur,Clawback, on = "Month", direction = "backward").set_index(Proj.MP().index)
    return rate["Projection"] * (Proj.DUR_M(t) <= claw_mth["Clawback Month"])


def COHORT():

    """The cohort of the model points"""

    return Proj.MP()["PCODE"]


# ---------------------------------------------------------------------------
# References

exp_acq = ("IOSpec", 2470942121872, 2470942121872)

exp_claim = ("IOSpec", 2470957259152, 2470957259152)

exp_maint = ("IOSpec", 2470957257520, 2470957257520)

infl_rate = ("IOSpec", 2470957264816, 2470957264816)

mad = ("IOSpec", 2470957264528, 2470957264528)

model_path = ("IOSpec", 2470957262512, 2470957262512)

mort_scale = ("IOSpec", 2470957258864, 2470957258864)

res_exp_acq = ("IOSpec", 2470960571984, 2470960571984)

res_exp_claim = ("IOSpec", 2470957257280, 2470957257280)

res_exp_maint = ("IOSpec", 2470960130864, 2470960130864)

res_infl_rate = ("IOSpec", 2470960133504, 2470960133504)

res_mort_scale = ("IOSpec", 2470960125968, 2470960125968)

SM_Rates = ("IOSpec", 2470960128416, 2470960128416)

tax_rates = ("IOSpec", 2470960128224, 2470960128224)

SM_RES_DPF = ("IOSpec", 2470960122368, 2470960122368)

claw_ind = ("IOSpec", 2470960238256, 2470960238256)

claw_mth = ("IOSpec", 2470960243488, 2470960243488)

ST_rate = ("IOSpec", 2470960240848, 2470960240848)

UF_FMC = ("IOSpec", 2470960244688, 2470960244688)

admin_chg_cap = ("IOSpec", 2470960235568, 2470960235568)

surr_band = ("IOSpec", 2470960878432, 2470960878432)

surr_mth = ("IOSpec", 2470960878624, 2470960878624)

res_UF_FMC = ("IOSpec", 2470960878816, 2470960878816)

res_mort_chg_pc = ("IOSpec", 2470960878960, 2470960878960)

min_DB = ("IOSpec", 2470960879200, 2470960879200)

Lapse = ("IOSpec", 2470960889136, 2470960879440)

Commission = ("IOSpec", 2470960884000, 2470960879344)

YieldCurve = ("IOSpec", 2470960882560, 2470960875408)

Mortality = ("IOSpec", 2470960924848, 2470960879536)

ChargeMort = ("IOSpec", 2470960881792, 2470960936416)

AllocCharge = ("IOSpec", 2470960884288, 2470960881888)

AdminCharge = ("IOSpec", 2470960885728, 2470960882368)

SurrCharge = ("IOSpec", 2470960932336, 2470960881504)

SurrChargeCap = ("IOSpec", 2470960926000, 2470960889328)

Clawback = ("IOSpec", 2470962312528, 2470960937088)

PartialWithdrawal = ("IOSpec", 2470960936224, 2470960883280)

LoyaltyAdd = ("IOSpec", 2470961727376, 2470960882080)

PremHoliday = ("IOSpec", 2470962304368, 2470960925280)

pd = ("Module", "pandas")

np = ("Module", "numpy")

model_point_table = ("IOSpec", 2470961740528, 2470960938288)

Proj = ("Interface", ("..", "Projection"), "auto")

inspect = ("Module", "inspect")

mort_chg_scale = ("IOSpec", 2470960884816, 2470960884816)

res_IR = ("IOSpec", 2470961732128, 2470961732128)

point_id = 0