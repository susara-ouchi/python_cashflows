from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def COHORT():

    """The cohort of the model points"""

    return Proj.MP()["PCODE"]


# ---------------------------------------------------------------------------
# References

inspect = ("Module", "inspect")

pd = ("Module", "pandas")

np = ("Module", "numpy")

model_point_table = ("IOSpec", 2239005592448, 2239000050224)

exp_acq = ("IOSpec", 2239005591632, 2239005591632)

exp_claim = ("IOSpec", 2239005596192, 2239005596192)

exp_maint = ("IOSpec", 2239010703776, 2239010703776)

infl_rate = ("IOSpec", 2239005591728, 2239005591728)

mad = ("IOSpec", 2239011003728, 2239011003728)

mort_scale = ("IOSpec", 2239010996480, 2239010996480)

res_exp_acq = ("IOSpec", 2239010996576, 2239010996576)

res_exp_claim = ("IOSpec", 2239010996864, 2239010996864)

res_exp_maint = ("IOSpec", 2239010997056, 2239010997056)

res_infl_rate = ("IOSpec", 2239010997152, 2239010997152)

res_IR = ("IOSpec", 2239010914016, 2239010914016)

res_mort_scale = ("IOSpec", 2239011003776, 2239011003776)

SM_Rates = ("IOSpec", 2239011153584, 2239011153584)

Tax_Rates = ("IOSpec", 2239011153392, 2239011153392)

mat_fac = ("IOSpec", 2239011159488, 2239011159488)

model_path = ("IOSpec", 2239011153680, 2239011153680)

math = ("Module", "math")

SurrTerm = ("IOSpec", 2239011153440, 2239011153440)

GSV_Factor = ("IOSpec", 2239011201536, 2239011206048)

mort_table = ("IOSpec", 2239011002240, 2239011199808)

yield_curve = ("IOSpec", 2239011000848, 2239010999504)

IncomeBenefit = ("IOSpec", 2239011789920, 2239011002096)

lapse_table = ("IOSpec", 2239012566112, 2239011208016)

comm_rates = ("IOSpec", 2239011794528, 2239012561072)

point_id = 0

Proj = ("Interface", ("..", "Projection"), "auto")