# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 20:39:16 2023

@author: vineet.gupta

creates a list of functions with their description
"""

import os
import modelx as mx
import pandas as pd

os.chdir(os.path.dirname(__file__))

names = []; formulas = []
temp = ""; temp1 = ""; temp2 = ""
MyModel = mx.read_model("model")
for space in MyModel.spaces.keys():
    exec(f"temp = MyModel.{space}.cells")
    for cell in list(temp):
        exec(f"temp1 = MyModel.{space}.{cell}.fullname")
        names.append(temp1)
        exec(f"temp2 = str(MyModel.{space}.{cell}.doc)")
        formulas.append(temp2)
del(space, cell, temp, temp1, temp2)
df = pd.DataFrame({'Name': names, "Formulas": formulas})
del(names, formulas)
df.to_csv(f"{MyModel.Input.model_path['Path']}\\formulas.csv")
del(df)