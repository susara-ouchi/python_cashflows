from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def RESULTS(export: bool = True, name: str = "results", file_type: str = ".csv"):

    """All results
        export (bool): whether to export the results (setting this to False returns the pd.Dataframe)
        name (str): name to the file being exported
        file_type (str): set to '.csv' by default. Other option is '.xlsx'
    """

    from datetime import datetime
    print(f"{Input.inspect.stack()[0][3]}({export}, {name}) called at: {datetime.now().strftime('%H:%M:%S')}")

    t_len = range(Projection.PROJ_LEN().max())
    Data = dict(); DataColumns = []; ExtendedFx = []#; DataColumnsTypeError = []
    elements = {"Input": list(Input.cells),
                "COBFactor": list(COBFactor.cells),
                "AssetShare": list(AssetShare.cells),
                "Reserves": list(Reserves.cells),
                "Projection": list(Projection.cells)}

    for userspace in elements:
        for cell in elements[userspace]:
            if eval(f"{userspace}.{cell}.parameters == ('t',)"):
                DataColumns.append(f"{userspace}.{cell}")
            elif eval(f"{userspace}.{cell}.parameters == ()"):
                pass
            elif f"{userspace}.{cell}" not in ForbiddenCells:
                ExtendedFx.append(f"{userspace}.{cell}")

    for DataColumn in tqdm(DataColumns):
        if DataColumn not in ExtendedFx:
            try:
                Data[DataColumn] = Input.pd.Series([eval(f"sum({DataColumn}({t}))") for t in t_len], index = t_len)
            except TypeError as e:
                Data[DataColumn] = Input.pd.Series([eval(f"{DataColumn}({t})") for t in t_len], index = t_len)
    #if len(DataColumnsTypeError) > 0: print(f"\nTypeError: {DataColumnsTypeError}")
        else:
            args = eval(f'{DataColumn}.doc.replace(" ", "").split(",")')
            for arg in args:
                try:
                    Data[f"{DataColumn}({arg})"] = Input.pd.Series([eval(f"sum({DataColumn}({t}, '{arg}'))") for t in t_len], index = t_len)
                except TypeError as e:
                    Data[f"{DataColumn}({arg})"] = Input.pd.Series([eval(f"{DataColumn}({t}, '{arg}')") for t in t_len], index = t_len)

    DF = Input.pd.DataFrame.from_dict(Data)
    if export == True:
        try:
            if name == "": name = str('%.0e'%len(Input.model_point_table.index)).replace("+","")
            path = Input.model_path["Path"] + f"\\{name}" + file_type

            if file_type == ".csv":
                DF.to_csv(path); del(DF)
            elif file_type == ".xlsx":
                DF.to_excel(path); del(DF)
            else:
                raise TypeError("invalid file type passed")
            return f"{Input.inspect.stack()[0][3]} exported successfully!"
        except PermissionError as e:
            raise PermissionError(f"The file '{name}{file_type}' is being used by another process.")
    else:
        return DF


def PROFIT_MARGIN():

    """Profit Margin
    defined as - VIF(0)/Premium

    in percentage terms"""

    return (Projection.VIF[0]/Projection.PREM_PP()) * 100


def COHORT(name: str = "cohorts", file_type: str = ".xlsx"):

    """Cohort Results
        name (str)(optional): name to the file being exported
        file_type (str)(optional): set to '.xlsx' by default. Other option is '.csv'
    """

    from datetime import datetime
    print(f"{Input.inspect.stack()[0][3]}({name}{file_type}) called at: {datetime.now().strftime('%H:%M:%S')}")

    t_len = range(Projection.PROJ_LEN().max())
    DataColumns = []; ExtendedFx = []; ForbiddenCells = []
    COHORT = Input.COHORT(); CohortSet = list(set(COHORT)); CohortSet.sort()

    def CohortSum(x: Input.pd.Series):
        var = x.copy()
        var.index = COHORT
        return var.groupby(var.index).sum()

    for i in CohortSet:
        exec(f"Data_{i} = dict()")

    elements = {"Input": list(Input.cells),
                "COBFactor": list(COBFactor.cells),
                "AssetShare": list(AssetShare.cells),
                "Reserves": list(Reserves.cells),
                "Projection": list(Projection.cells),
                }

    for userspace in elements:
        for cell in elements[userspace]:
            if eval(f"{userspace}.{cell}.parameters == ('t',)"):
                DataColumns.append(f"{userspace}.{cell}")
            elif eval(f"{userspace}.{cell}.parameters == ()"):
                pass
            elif f"{userspace}.{cell}" not in ForbiddenCells:
                ExtendedFx.append(f"{userspace}.{cell}")

    for DataColumn in tqdm(DataColumns+ExtendedFx):
        if DataColumn not in ExtendedFx:
            Multi_Str = "".join([f"Data_{i}['{DataColumn}']," for i in CohortSet])
            try:
                temp = Input.np.array(Input.pd.Series([eval(f"{DataColumn}({t})") for t in t_len], index = t_len).apply(CohortSum)).transpose()
                exec(f"{Multi_Str} = temp"); del(temp)
            except (TypeError, AttributeError):
                for i in CohortSet:
                    temp = Input.pd.Series([eval(f"{DataColumn}({t})") for t in t_len], index = t_len)
                    exec(f"Data_{i}['{DataColumn}'] = temp"); del(temp)
        else:
            args = eval(f'{DataColumn}.doc.replace(" ", "").split(",")')
            for arg in args:
                Multi_Str = "".join([f"Data_{i}['{DataColumn}({arg})']," for i in CohortSet])
                try:
                    temp = Input.np.array(Input.pd.Series([eval(f"{DataColumn}({t}, '{arg}')") for t in t_len], index = t_len).apply(CohortSum)).transpose()
                    exec(f"{Multi_Str} = temp"); del(temp)
                except (TypeError, AttributeError):
                    for i in CohortSet:
                        temp = Input.pd.Series([eval(f"{DataColumn}({t}, '{arg}')") for t in t_len], index = t_len)
                        exec(f"Data_{i}['{DataColumn}({arg})'] = temp"); del(temp)

    if file_type == ".csv":
        for i in CohortSet:
            DF = eval(f"Input.pd.DataFrame.from_dict(Data_{i})"); exec(f"del(Data_{i})")
            filename = f"{name}_{i}" + file_type
            path = Input.model_path["Path"] + "\\" + filename
            try:
                DF.to_csv(path)
            except PermissionError:
                raise PermissionError(f"The file '{filename}' is being used by another process")
            del(DF, path, filename)
        return f"{Input.inspect.stack()[0][3]} exported successfully!"
    elif file_type == ".xlsx":
        filename = f"{name}" + file_type
        path = Input.model_path["Path"] + "\\" + filename
        with Input.pd.ExcelWriter(path) as w:
            try:
                for i in CohortSet:
                    DF = eval(f"Input.pd.DataFrame.from_dict(Data_{i})"); exec(f"del(Data_{i})")
                    DF.to_excel(w, sheet_name = f"{COHORT.name}_{i}")
                return f"{Input.inspect.stack()[0][3]} exported successfully!"
            except PermissionError:
                raise PermissionError(f"The file '{filename}' is being used by another process")


# ---------------------------------------------------------------------------
# References

tqdm = ("Pickle", 2470921057568)

Input = ("Interface", ("..", "Input"), "auto")

Projection = ("Interface", ("..", "Projection"), "auto")

Reserves = ("Interface", ("..", "Reserves"), "auto")

COBFactor = ("Interface", ("..", "COBFactor"), "auto")

AssetShare = ("Interface", ("..", "AssetShare"), "auto")