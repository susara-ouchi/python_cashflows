from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = [
    "Actuals"
]

# ---------------------------------------------------------------------------
# Cells

def AGE(t):
    """The attained age at time t."""
    if t < 0:
        raise ValueError("t cannot be less than 0")
    else:
        n = Mortality.index.max()
        return np.minimum(AGE_AT_ENTRY() + DUR_Y(t-1), n)


def AGE_AT_ENTRY():
    """The age at entry of the selected model point"""

    return MP()["IssueAge"]


def ASSM_CHG_RUN(assm):
    """Determines which scenario relates to assumption
        change for the given assumption

    Returns -1 by default

    assm: Inflation, Mortality
    """

    try:
        temp = AssumptionsMatrix[assm]
        return min(temp[temp!=temp[0]].index)
    except:
        return 0


def AST_EARN_RATE_M(t, basis):
    """Monthly Assets Earned Rate

    basis: Locked, Previous, Current"""

    return (1 + AssetEarnedRate[basis][math.ceil(t/12)])**(1/12) - 1


def BASE_MORT_RATE(t, basis):
    """Base mortality rates at time t

    basis: Locked, Previous, Current"""

    ages = list(AGE(t)); sex = list(eval(f"Mortality.{basis}.columns"))
    mort_rates = 0

    for i in sex:
        mort_rates += (SEX() == i) * list(eval(f"Mortality.{basis}[i][ages]"))

    return pd.Series(mort_rates, name = inspect.stack()[0][3])


def COHORT():
    """The cohort of the model points"""

    return MP()["PCODE"]


def COMM_RATE(t):
    """Lapse rate"""

    n = Commissions.index.max()
    dur_m = list(np.minimum((DUR_M(t)/12).apply(math.ceil), n))
    comm_rates = Commissions["Projection"][dur_m]

    return pd.Series(list(comm_rates), index = MP().index)


def DISC_RATE_M(t, basis):
    """Monthly discount rate

   basis: Locked, Previous, Current"""

    return (1 + DiscountRate[basis][math.ceil(t/12)])**(1/12) - 1


def DUR_M(t):
    """Duration in force in months"""

    if t <= 0:
        return pd.Series(0, index = MP().index)
    else:
        return DUR_M(t-1) + 1


def DUR_Y(t):
    """Duration in force in years"""

    return DUR_M(t)//12


def INCM_FAC(t):
    """Income factor: as a percentage of premium.
    Used for calculation of PV_DB, PV_INCM_BEN
    Applicable for duration `PREM_TERM < y < POL_TERM`"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return pd.Series(0, index = MP().index)
    else:
        ppt = list(MP().PremPayingTerm.unique())
        ages = list(AGE_AT_ENTRY())
        First5Years = 0; Last5Years = 0

        flag = (DUR_M(t) > PREM_TERM_M()) * (DUR_M(t) <= POL_TERM_M())

        for i in ppt:
            First5Years += (PREM_TERM_Y() == i) * list(IncomeBenefit[i]["First 5 years"][ages])
            Last5Years += (PREM_TERM_Y() == i) * list(IncomeBenefit[i]["Last 5 years"][ages])

        rates = ((DUR_M(t) <= POL_TERM_M() - 12 * 5) * First5Years
                 + (DUR_M(t) > POL_TERM_M() - 12 * 5) * Last5Years)

    return flag * rates


def INFL_FAC(t, basis):
    """The inflation factor at time t

    basis: Locked, Previous, Current"""

    if t <= 0:
        return 1
    else:
        return (1 + INFL_RATE(basis)) ** ((t-1)/12)


def INFL_RATE(basis):
    """Inflation rate

    basis: Locked, Previous, Current"""

    return Inflation[basis]


def INIT_POLS_IF(): 
    """Initial Number of Policies In-force

    Number of in-force policies at time 0 referenced from :func:`pols_if`.
    Defaults to 1."""

    return MP()["PolicyCount"]


def LAPSE_RATE_ANN(t):
    """Lapse rate"""

    n = Lapses.index.max()
    dur_m = list(np.minimum((DUR_M(t)/12).apply(math.ceil), n))
    lapse_rates = Lapses["Projection"][dur_m]

    return pd.Series(list(lapse_rates), index = MP().index)


def LAPSE_RATE_MLY(t):
    """Lapse rate"""

    return (1 - (1 - LAPSE_RATE_ANN(t))**(1/12))


def LOAD_TABLES(*tables):

    """Update tables added to the table files

    tables: table files to be updated
    Example - LOAD_TABLES('table1', 'table2')

    returns 0
    """

    print(f"\n{inspect.stack()[0][3]}({tables[0]}) called at: {datetime.datetime.now().strftime('%H:%M:%S')}")

    for table in tables[0]:
        if not os.path.isabs(Path[table]):
            table_path = os.path.join(Path["Model"], Path[table])
        else:
            raise ValueError("relative path required for tables/excel range files")

        table_workbook = openpyxl.load_workbook(filename = table_path)
        for sheet in table_workbook.sheetnames:
            if sheet not in dir(LOAD_TABLES.parent):
                df = pd.read_excel(table_path, sheet_name = sheet, index_col = 0, header = 0)
                LOAD_TABLES.parent.new_pandas(data = df, file_type = "excel", name = sheet, path = Path[table], sheet = sheet)
                if eval(f"{sheet}.isnull().values.any()"):
                    status = "Wrn"
                else:
                    status = "OK"
                print(f"Loaded {sheet}... {status}")
    return 0


def LOAD_XLRANGES(table, sheet):

    """Update ranges added to the excel range files

    table: table file to be updated
    sheet: name of the sheet
    Example - LOAD_XLRANGES('Range1', 'Sheet1')

    Note: do not include relavant data in first row of excel sheet

    returns 0
    """

    from xlsxwriter.utility import xl_col_to_name

    if not os.path.isabs(Path[table]):
        table_path = os.path.join(Path["Model"], Path[table])
    else:
        raise ValueError("relative path required for tables/excel range files")

    df = pd.read_excel(table_path, sheet_name = sheet)
    df = df.mask(df.applymap(lambda s: "#" in s if isinstance(s, str) else False))
    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            if isinstance(df.iat[i, j], str) and (pd.isna(df.iat[i, j+1]) and (j == 0 or pd.isna(df.iat[i, j-1]))):
                k = 0; cond1 = True
                while True:
                    try:
                        cond1 = pd.isna(df.iat[i+k+1, j])
                        if cond1:
                            break
                        else:
                            k += 1
                    except IndexError:
                        break
                rangename = df.iat[i, j]
                range1 = f"{xl_col_to_name(j)}{i+3}:{xl_col_to_name(j+1)}{i+k+2}"
                if rangename not in dir(LOAD_XLRANGES.parent):
                    LOAD_XLRANGES.parent.new_excel_range(name = rangename, path = Path[table], range_ = range1, sheet = sheet, keyids = ['c0'])
                    print(f"Loaded {rangename}...")

    return 0


def MAX_PROJ_LEN():
    return PROJ_LEN().max()+1


def MAX_SCEN():
    """Maximum number of scenarios to run for assumption changes"""

    return max(AssumptionsMatrix.index)


def MORT_RATE_ANN(t, basis):
    """Mortality rate to be applied at time t

    basis: Locked, Previous, Current"""

    fac = Mort_Scale["Rate"]
    return fac * BASE_MORT_RATE(t, basis)


def MORT_RATE_MLY(t, basis):
    """Monthly mortality rate to be applied at time t

    basis: Locked, Previous, Current"""

    return 1 - (1 - MORT_RATE_ANN(t, basis))**(1/12)


def MP():
    """The selected model point as a Series"""

    if type(point_id) == int:
        if point_id == 0:
            return ModelPointsFile
        else:
            return ModelPointsFile.loc[[point_id]]
    elif type(point_id) == list:
        return ModelPointsFile.loc[point_id]
    elif type(point_id) == range:
        return ModelPointsFile.loc[list(point_id)]    
    else:
        raise ValueError(f"Incompatible data type for Input.point_id: {type(point_id)}")


def POL_TERM_M():
    """The policy term of the selected model point."""

    return POL_TERM_Y() * 12


def POL_TERM_Y():
    """The policy term of the selected model point.

    The element labeled ``policy_term`` of the Series returned by
    :func:`model_point`."""

    return MP()["PolicyTerm"]


def PREM_PP():
    """Annual premium per policy"""

    return MP()["AnnPrem"]


def PREM_TERM_M():
    """Premium paying term in months"""

    return 12 * PREM_TERM_Y()


def PREM_TERM_Y():
    """Premium paying term in years"""

    return MP()["PremPayingTerm"]


def PREP_INPUTS():
    """Runs all input variables

    In "ForbiddenCells", the user can add cells
    they wish to not include in results"""

    ForbiddenCells = ["LOAD_TABLES", "PREP_INPUTS", "LOAD_XLRANGES"]

    t_len = range(1, MAX_PROJ_LEN() + 1)
    elements = {"Input": list(PREP_INPUTS.parent.cells),}

    ## DO NOT MODIFY ##
    DataColumns, ExtendedFx = list(), list()

    print("Preparing Inputs...")

    #### main loop starts here ####

    for userspace in elements:
        for cell in elements[userspace]:
            if eval(f"{cell}.parameters == ('t',)"):
                DataColumns.append(f"{cell}")
            elif eval(f"{cell}.parameters == ()"):
                pass
            elif f"{cell}" not in ForbiddenCells:
                ExtendedFx.append(f"{cell}")

    for DataColumn in (DataColumns+ExtendedFx):
        if DataColumn not in ExtendedFx:
            try:
                pd.Series([eval(f"{DataColumn}({t})") for t in t_len], index = t_len)
            except TypeError as e:
                eval(f"{DataColumn}()")
        else:
            params = eval(f'{DataColumn}.parameters')
            for param in params[1:]:
                doc = eval(f'{DataColumn}.doc')
                args = doc[doc.find(param)+len(param)+1:].replace(" ", "").split(",")
                for arg in args:
                    pd.Series([eval(f"{DataColumn}({t}, '{arg}')") for t in t_len], index = t_len)
    return 0


def PROJ_LEN():
    """Projection length in months

    Projection length in months defined as::

        12 * policy_term() + 1 """

    return POL_TERM_M() - DUR_M(0) + 2


def SEX(): 
    """The sex of the selected model point(s)"""

    return MP()["Sex"]


def SUM_ASSURED():
    """The sum assured of the selected model point(s)"""

    return MP()["SumAssured"]


def SURR_TERM():
    """Term in months till which the surrender value is 0"""

    return PREM_TERM_Y()/6 * 12


def TERMINAL_BEN():
    """Terminal benefit"""

    mat_fac = pd.Series([Maturity_Factor[POL_TERM_Y()[i]] for i in MP().index], index = MP().index)
    #return SUM_ASSURED() * (mat_fac/10)
    return SUM_ASSURED() * (1 + mat_fac/10)


def VAL_M():
    """Policy month when valuation is done"""

    dt = datetime.datetime
    return ( (Valuation["Date"] - MP()['IssueYear'].apply(lambda i: dt(i, 1, 1)))
            .apply(lambda i: round(i.days/30)) )


# ---------------------------------------------------------------------------
# References

xlsxwriter = ("Module", "xlsxwriter")

inspect = ("Module", "inspect")

pd = ("Module", "pandas")

np = ("Module", "numpy")

math = ("Module", "math")

os = ("Module", "os")

openpyxl = ("Module", "openpyxl")

ModelPointsFile = ("IOSpec", 2763548782016, 2763548780816)

Mort_Scale = ("IOSpec", 2763548779712, 2763548779712)

Res_Int_Rate = ("IOSpec", 2763545566752, 2763545566752)

Mad = ("IOSpec", 2763549586960, 2763549586960)

Exp_Acq_A = ("IOSpec", 2763549588928, 2763549588928)

Exp_Acq_NA = ("IOSpec", 2763549589168, 2763549589168)

Exp_Maint_A = ("IOSpec", 2763549588304, 2763549588304)

EXP_Maint_NA = ("IOSpec", 2763549585856, 2763549585856)

Exp_Claim_A = ("IOSpec", 2763549586624, 2763549586624)

Res_Inflation = ("IOSpec", 2763550056512, 2763550056512)

SolvM = ("IOSpec", 2763550056896, 2763550056896)

Maturity_Factor = ("IOSpec", 2763549278800, 2763549278800)

Commissions = ("IOSpec", 2763548055008, 2763549279616)

GSVFactors = ("IOSpec", 2763549578288, 2763548881296)

Lapses = ("IOSpec", 2763549580640, 2763549243568)

RiskAdjustment = ("IOSpec", 2763551573808, 2763548779280)

IncomeBenefit = ("IOSpec", 2763552269456, 2763550051152)

Path = ("IOSpec", 2763552277648, 2763552277648)

Valuation = ("IOSpec", 2763551270992, 2763551270992)

datetime = ("Module", "datetime")

Inflation = ("IOSpec", 2763549568880, 2763549568880)

DiscountRate = ("IOSpec", 2763551347472, 2763549579104)

AssetEarnedRate = ("IOSpec", 2763551894832, 2763549578768)

AssumptionsMatrix = ("IOSpec", 2763551892816, 2763549579680)

Mortality = ("IOSpec", 2763552566912, 2763542427776)

point_id = 0