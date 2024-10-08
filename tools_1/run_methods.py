# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 19:19:12 2022
"""

import time
import modelx as mx
import numpy as np
from math import ceil
import pandas as pd

def run_model(modelpath: str, export: bool, OutputPath: str, batchsize: int = int(5e4),
              file_type: str = ".csv"):
    """calls RESULTS function from model; if model point table is too large, runs batch-wise

    Args:
        modelpath (string): Path to the model folder
        export (bool): Whether the results are to be exported
        OutputPath (str): a single folder to all the results
        batchsize (int, optional): Maximum size of a batch. Defaults to 5e4.
        file_type (str, optional): default is '.csv'; another option is '.xlsx'
    Returns:
        pd.Dataframe: if export is False
    """
 
    StartTime = time.time()
    
    MAX = min(batchsize, int(float(2e5))); modelname = modelpath[modelpath.rfind("\\") + 1:]
    print(f"Running model: {modelname}")

    MyModel = mx.read_model(modelpath); del(modelpath)
    MyModel.Input.model_path["Path"] = OutputPath
    AllModelPoints = MyModel.Input.model_point_table.index
    LengthMPTable = len(AllModelPoints)

    FileName = modelname+"_aggregate"
    if LengthMPTable <= MAX:
        MyModel.Input.point_id = 0
        MyModel.Output.RESULTS(export, FileName, file_type)
        MyModel.Input.point_id = 0
        del(AllModelPoints, LengthMPTable, FileName, MyModel, export)
    else:
        MPBatches = np.array_split(AllModelPoints, ceil(LengthMPTable/MAX))
        del(AllModelPoints, LengthMPTable)
        for i in range(len(MPBatches)):
            MyModel.Input.point_id = list(MPBatches[i])
            if i == 0:
                df = MyModel.Output.RESULTS(False, f"{i+1}/{len(MPBatches)}")
            else:
                df = df.add(MyModel.Output.RESULTS(False, f"{i+1}/{len(MPBatches)}"))
        MyModel.Input.point_id = 0
        del(i)

        if export:
            try:
                if file_type == ".csv":
                    df.to_csv(f"{OutputPath}/{FileName}.csv"); del(FileName, df, OutputPath)
                elif file_type == ".xlsx":
                    df.to_excel(f"{OutputPath}/{FileName}.xlsx"); del(FileName, df, OutputPath)
                MyModel.Input.point_id = 0; del(MyModel)
            except PermissionError as e:
                MyModel.Input.point_id = 0; del(MyModel)
                raise PermissionError(f"{e}: File is currently being used by another process.")
        else:
            MyModel.Input.point_id = 0; del(MyModel)
            return df
    
    print(f"\nTotal time taken: {round(time.time()-StartTime, 2)}s"); del(StartTime)

def stack_tracing(modelpath: str, export: bool, OutputPath: str, file_type: str = ".csv"):
    """Generates runtime report for Python models

    Args:
        modelpath (string): path to the model folder
        export (bool): Whether the results file are to be exported
        OutputPath (str): a single folder to all the results
        file_type (str, optional): default is '.csv'; another option is '.xlsx'
    """

    StartTime = time.time()
    modelname = modelpath[modelpath.rfind("\\") + 1:]
    FileName = modelname+"_aggregate"; del(modelname)
    StackTraceFile = f"{FileName}_report"
    
    ## read the model
    MyModel = mx.read_model(modelpath); del(modelpath)
    MyModel.Input.model_path["Path"] = OutputPath

    ## setup formula trace
    MyModel.time = time
    mx.start_stacktrace(maxlen = None)

    ## run the model
    MyModel.Input.point_id = 0
    
    MyModel.Output.RESULTS(export, FileName, file_type)
    MyModel.Input.point_id = 0

    print(f"Model run time: {round(time.time() - StartTime, 2)}s")
    df = pd.DataFrame.from_dict(mx.get_stacktrace(summarize = True))

    ## format dataframe and export post runtime data
    try:
        if file_type == ".csv":
            df[:-2].transpose().to_csv(f"{OutputPath}/{StackTraceFile}.csv")
        elif file_type == ".xlsx":
            df[:-2].transpose().to_xlsx(f"{OutputPath}/{StackTraceFile}.xlsx")
        MyModel.Input.point_id = 0; del(MyModel)
    except PermissionError as e:
        MyModel.Input.point_id = 0; del(MyModel)
        raise PermissionError(f"{e}: File is currently being used by another process.")
    mx.stop_stacktrace()

    print(f"\nTotal time taken: {round(time.time()-StartTime, 2)}s")
    del(df, StackTraceFile, StartTime)
    
def cohort_model(modelpath: str, OutputPath: str, file_type: str = ".xlsx"):
    """calls COHORT function from model

    Args:
        modelpath (string): Path to the model folder
        OutputPath (str): a single folder to all the results
        file_type (str, optional): default is '.csv'; another option is '.xlsx'
    Returns:
        pd.Dataframe: if export is False
    """
 
    StartTime = time.time()
    modelname = modelpath[modelpath.rfind("\\") + 1:]
    print(f"Running model: {modelname}")

    MyModel = mx.read_model(modelpath); del(modelpath)
    MyModel.Input.model_path["Path"] = OutputPath; del(OutputPath)

    FileName = modelname+"_cohort"
    MyModel.Input.point_id = 0
    MyModel.Output.COHORT(FileName, file_type)
    MyModel.Input.point_id = 0
    del(FileName, MyModel)
    
    print(f"\nTotal time taken: {round(time.time()-StartTime, 2)}s"); del(StartTime)