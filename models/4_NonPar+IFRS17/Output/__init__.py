from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def AGGREGATE_CF(export = None, name: str = "aggregate", file_type: str = ".csv"):

    """Aggregate results
        export (bool)(optional): whether to export the results (setting this to False returns the pd.Dataframe)
        name (str)(optional): name to the file being exported
        file_type (str)(optional): set to '.csv' by default. Other option is '.xlsx'

        In "ForbiddenCells" and "ForbiddenSpaces", the user can add cells and spaces
        they wish to not include in results
    """

    from datetime import datetime
    Input.PREP_INPUTS()

    print(f"{Input.inspect.stack()[0][3]}({export}, {name}) called at: {datetime.now().strftime('%H:%M:%S')}")

    """ Variables Declaration """
    ForbiddenCells, ForbiddenSpaces = [], [] ## User can modify as required -- see documentation

    t_len = range(Input.MAX_PROJ_LEN())
    scenarios = list(Input.AssumptionsMatrix.index) ## PolicyProjection.BestEstimateRebased

    ## DO NOT MODIFY ##
    Data, DataColumns, elements, ExtendedFx, spaces = dict(), list(), dict(), list(), list()

    """ Functions Declaration """
    def GiveSpaces(x, y):
        s = eval(f"list({x}.spaces)")
        if len(list(s)) > 0:
            for i in s:
                y.append(f"{x}.{i}")
                GiveSpaces(f"{x}.{i}", y)
    GiveSpaces("PolicyProjection", spaces)

    for i in ForbiddenSpaces:
        if i in spaces:
            spaces.remove(i)

    for space in spaces:
        if eval(f"{space}.parameters") == ():
            elements[space] = list(eval(f"{space}.cells"))
        else:
            for scen in scenarios: ## for multiple runs during Rebasing
                elements[f"{space}({scen})"] = list(eval(f"{space}({scen}).cells"))

    for userspace in elements:
        for cell in elements[userspace]:
            if eval(f"{userspace}.{cell}.parameters == ('t',)"):
                DataColumns.append(f"{userspace}.{cell}")
            elif eval(f"{userspace}.{cell}.parameters == ()"):
                pass
            elif f"{userspace}.{cell}" not in ForbiddenCells:
                ExtendedFx.append(f"{userspace}.{cell}")

    #### main loop starts here ####

    for DataColumn in tqdm(DataColumns+ExtendedFx):
        if DataColumn not in ExtendedFx:
            try:
                Data[DataColumn] = Input.pd.Series([eval(f"sum({DataColumn}({t}))") for t in t_len], index = t_len)
            except TypeError as e:
                Data[DataColumn] = Input.pd.Series([eval(f"{DataColumn}({t})") for t in t_len], index = t_len)
        else:
            args = eval(f'{DataColumn}.doc.replace(" ", "").split(",")') ## to be updated - refer PREP_INPUTS()
            for arg in args:
                try:
                    Data[f"{DataColumn}({arg})"] = Input.pd.Series([eval(f"sum({DataColumn}({t}, '{arg}'))") for t in t_len], index = t_len)
                except TypeError as e:
                    Data[f"{DataColumn}({arg})"] = Input.pd.Series([eval(f"{DataColumn}({t}, '{arg}')") for t in t_len], index = t_len)

    DF = Input.pd.DataFrame.from_dict(Data)

    #### export methods ####

    if export == True:
        try:
            if name == "": name = str('%.0e'%len(Input.ModelPointsFile.index)).replace("+","")
            path = Input.os.path.join(Input.Path["Results"], name + file_type)

            if file_type == ".csv":
                DF.to_csv(path); del(DF)
            elif file_type == ".xlsx":
                DF.to_excel(path); del(DF)
            else:
                raise TypeError("invalid file type passed")
            return f"{Input.inspect.stack()[0][3]} exported successfully!"
        except PermissionError as e:
                raise PermissionError(f"{e}: The file '{name}{file_type}' is being used by another process.")
    elif export == False:
        return DF
    elif export == None:
        return 0


def SET_COHORT():

    """Ensures that policies are cohorted properly

        Note: a suffix of 0/1 is a boolean for
        whether the policy is non-onerous
    """
    AGGREGATE_CF()

    if Input.MP()["PCODE"].isna().any():
        cohort = ("COH_"
                  + Input.MP()["IssueYear"].apply(str)
                  + "_"
                  + PolicyProjection.InitRecog.NON_ONEROUS().apply(str)).rename("COHORT")

        if Input.point_id != 0:
            raise Warning("Only a subset of the model points file has been selected.")

        Input.ModelPointsFile["PCODE"] = cohort
    return 0


def COHORT_CF(export = None, name: str = "cohorts", file_type: str = ".xlsx"):

    """Cohort Results
        export (bool)(optional): whether to export the results or not
        name (str)(optional): name to the file being exported
        file_type (str)(optional): set to '.xlsx' by default. Other option is '.csv'

        In "ForbiddenCells" and "ForbiddenSpaces", the user can add cells and spaces
        they wish to not include in results
    """

    from datetime import datetime
    if Input.MP()["PCODE"].isna().any():
        SET_COHORT()
    else:
        Input.PREP_INPUTS()

    print(f"{Input.inspect.stack()[0][3]}({export}, {name}, {file_type}) called at: {datetime.now().strftime('%H:%M:%S')}")

    """ Variables Declaration """
    ForbiddenCells, ForbiddenSpaces = [], [] ## User can modify as required -- see documentation

    t_len = range(Input.MAX_PROJ_LEN())
    scenarios = list(Input.AssumptionsMatrix.index) ## PolicyProjection.BestEstimateRebased

    ## DO NOT MODIFY
    Data, DataColumns, elements, ExtendedFx, spaces = dict(), list(), dict(), list(), list()
    COHORT = Input.MP()["PCODE"]; CohortSet = list(set(COHORT)); CohortSet.sort()

    """ Functions Declaration """
    def CohortSum(x: Input.pd.Series):
        var = x.copy()
        var.index = COHORT
        return var.groupby(var.index).sum()

    def GiveSpaces(x, y):
        s = eval(f"list({x}.spaces)")
        if len(list(s)) > 0:
            for i in s:
                y.append(f"{x}.{i}")
                GiveSpaces(f"{x}.{i}", y)
    GiveSpaces("PolicyProjection", spaces)

    for i in ForbiddenSpaces:
        if i in spaces:
            spaces.remove(i)

    for space in spaces:
        if eval(f"{space}.parameters") == ():
            elements[space] = list(eval(f"{space}.cells"))
        else:
            for scen in scenarios: ## for multiple runs during Rebasing
                elements[f"{space}({scen})"] = list(eval(f"{space}({scen}).cells"))

    for i in CohortSet:
        exec(f"Data_{i} = dict()")

    for userspace in elements:
        for cell in elements[userspace]:
            if eval(f"{userspace}.{cell}.parameters == ('t',)"):
                DataColumns.append(f"{userspace}.{cell}")
            elif eval(f"{userspace}.{cell}.parameters == ()"):
                pass
            elif f"{userspace}.{cell}" not in ForbiddenCells:
                ExtendedFx.append(f"{userspace}.{cell}")

    #### main loop starts here ####

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

    #### export methods ####

    if export == False:
        DF_Dict = dict()
        for i in CohortSet:
            DF = eval(f"Input.pd.DataFrame.from_dict(Data_{i})"); exec(f"del(Data_{i})")
            DF_Dict[i] = DF; del(DF)
        return DF_Dict

    elif export == True:
        if file_type == ".csv":
            for i in CohortSet:
                DF = eval(f"Input.pd.DataFrame.from_dict(Data_{i})"); exec(f"del(Data_{i})")
                filename = f"{i}" + file_type
                path = Input.os.path.join(Input.Path["Results"], filename)
                try:
                    DF.to_csv(path)
                except PermissionError:
                    raise PermissionError(f"The file '{filename}' is being used by another process")
                del(DF, path, filename)
            return f"{Input.inspect.stack()[0][3]} exported successfully!"
        elif file_type == ".xlsx":
            filename = f"{name}" + file_type
            path = Input.os.path.join(Input.Path["Results"], filename)
            with Input.pd.ExcelWriter(path) as w:
                try:
                    for i in CohortSet:
                        DF = eval(f"Input.pd.DataFrame.from_dict(Data_{i})"); exec(f"del(Data_{i})")
                        DF.to_excel(w, sheet_name = f"{i}")
                    return f"{Input.inspect.stack()[0][3]} exported successfully!"
                except PermissionError:
                    raise PermissionError(f"The file '{filename}' is being used by another process")
    elif export == None:
        return 0


def IFRS_RESULTS(export = None, name: str = "ifrs_results", file_type: str = ".xlsx"):

    """IFRS'17 Calculation results
        export (bool): whether to export results
        name (str)(optional): name to the file being exported
        file_type (str)(optional): set to '.xlsx' by default. Other option is '.csv'

        In "ForbiddenCells" and "ForbiddenSpaces", the user can add cells and spaces
        they wish to not include in results
    """

    from datetime import datetime
    COHORT_CF()

    print(f"{Input.inspect.stack()[0][3]}({name}{file_type}) called at: {datetime.now().strftime('%H:%M:%S')}")

    """ Variables Declaration """
    ForbiddenCells = ["IFRS17_Calc.BestEstimate.COHORT_VAR", "IFRS17_Calc.Actuals.COHORT_VAR"] ## + IFRS17_Calc.BestEstimateRebased[scen].COHORT_VAR
    ForbiddenSpaces = ["IFRS17_Calc.PVFCF"]

    t_len = range(Input.MAX_PROJ_LEN())
    COHORT = IFRS17_Calc.BestEstimate.COHORT().index; CohortSet = list(set(COHORT)); CohortSet.sort()
    scenarios = list(Input.AssumptionsMatrix.index) ## PolicyProjection.BestEstimateRebased

    ForbiddenCells += [f"IFRS17_Calc.BestEstimateRebased({scen}).COHORT_VAR" for scen in scenarios]

    ## DO NOT MODIFY ##
    DataColumns, elements, ExtendedFx, spaces = list(), dict(), list(), list()

    """ Functions Declaration """
    def CohortSum(x: Input.pd.Series):
        var = x.copy()
        var.index = COHORT
        return var.groupby(var.index).sum()

    def GiveSpaces(x, y):
        s = eval(f"list({x}.spaces)")
        if len(list(s)) > 0:
            for i in s:
                y.append(f"{x}.{i}")
                GiveSpaces(f"{x}.{i}", y)
    GiveSpaces("IFRS17_Calc", spaces)

    for i in ForbiddenSpaces:
        if i in spaces:
            spaces.remove(i)

    for i in CohortSet:
        exec(f"Data_{i} = dict()")

    for space in spaces:
        if eval(f"{space}.parameters") == () or eval(f"{space}.parameters") == None:
            elements[space] = list(eval(f"{space}.cells"))
        else:
            for scen in scenarios: ## for multiple runs during Rebasing
                elements[f"{space}({scen})"] = list(eval(f"{space}({scen}).cells"))

    for userspace in elements:
        for cell in elements[userspace]:
            if eval(f"{userspace}.{cell}.parameters == ('t',)"):
                DataColumns.append(f"{userspace}.{cell}")
            elif eval(f"{userspace}.{cell}.parameters == ()"):
                pass
            elif f"{userspace}.{cell}" not in ForbiddenCells:
                ExtendedFx.append(f"{userspace}.{cell}")

    #### main loop starts here ####

    for DataColumn in tqdm(DataColumns+ExtendedFx):
        if DataColumn not in ExtendedFx:
            Multi_Str = "".join([f"Data_{i}['{DataColumn}']," for i in CohortSet])
            try:
                temp = Input.np.array(Input.pd.Series([eval(f"{DataColumn}({t})") for t in t_len], index = t_len).apply(CohortSum)).transpose()
                exec(f"{Multi_Str} = temp"); del(temp)
            except (TypeError, AttributeError, ValueError):
                for i in CohortSet:
                    temp = Input.pd.Series([eval(f"{DataColumn}({t})") for t in t_len], index = t_len)
                    exec(f"Data_{i}['{DataColumn}'] = temp"); del(temp)

        ### parameterized formulas ###

        else:
            ## args = eval(f'{DataColumn}.doc.replace(" ", "").split(",")')
            params = eval(f'{DataColumn}.parameters')
            for param in params[1:]:
                doc = eval(f'{DataColumn}.doc')
                args = doc[doc.find(param)+len(param)+1:].replace(" ", "").split(",")

                for arg in args:
                    Multi_Str = "".join([f"Data_{i}['{DataColumn}({arg})']," for i in CohortSet])
                    try:
                        ## print("TESTING LOG: ", arg, type(arg))
                        ## print("TESTING CMD: ", f"{DataColumn}(t, '{arg}')")
                        temp = Input.np.array(Input.pd.Series([eval(f"{DataColumn}({t}, '{arg}')") for t in t_len], index = t_len).apply(CohortSum)).transpose()
                        exec(f"{Multi_Str} = temp"); del(temp)
                    except (TypeError, AttributeError):
                        for i in CohortSet:
                            temp = Input.pd.Series([eval(f"{DataColumn}({t}, '{arg}')") for t in t_len], index = t_len)
                            exec(f"Data_{i}['{DataColumn}({arg})'] = temp"); del(temp)

    #### export methods ####

    if export == False:
        DF_Dict = dict()
        for i in CohortSet:
            DF = eval(f"Input.pd.DataFrame.from_dict(Data_{i})"); exec(f"del(Data_{i})")
            DF_Dict[i] = DF; del(DF)
        return DF_Dict

    elif export == True:
        if file_type == ".csv":
            for i in CohortSet:
                DF = eval(f"Input.pd.DataFrame.from_dict(Data_{i})"); exec(f"del(Data_{i})")
                filename = f"{name}_{i}" + file_type
                path = Input.os.path.join(Input.Path["Results"], filename)
                try:
                    DF.to_csv(path)
                except PermissionError:
                    raise PermissionError(f"The file '{filename}' is being used by another process")
                del(DF, path, filename)
            return f"{Input.inspect.stack()[0][3]} exported successfully!"
        elif file_type == ".xlsx":
            filename = f"{name}" + file_type
            path = Input.os.path.join(Input.Path["Results"], filename)
            with Input.pd.ExcelWriter(path) as w:
                try:
                    for i in CohortSet:
                        DF = eval(f"Input.pd.DataFrame.from_dict(Data_{i})"); exec(f"del(Data_{i})")
                        DF.to_excel(w, sheet_name = f"{i}")
                    return f"{Input.inspect.stack()[0][3]} exported to '{filename}' successfully!"
                except PermissionError:
                    raise PermissionError(f"The file '{filename}' is being used by another process")
    elif export == None:
        return 0


# ---------------------------------------------------------------------------
# References

tqdm = ("Pickle", 2763493786096)

Input = ("Interface", ("..", "Input"), "auto")

IFRS17_Calc = ("Interface", ("..", "IFRS17_Calc"), "auto")

PolicyProjection = ("Interface", ("..", "PolicyProjection"), "auto")