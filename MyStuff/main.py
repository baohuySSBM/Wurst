from fastapi import FastAPI, HTTPException
from typing import Dict
from datetime import datetime
import pandas as pd

df = pd.read_csv("hardware_produkte.csv",sep=";",parse_dates=["MHD"],dayfirst = True)
df["MHD"] = df["MHD"].dt.strftime("%d.%m.%Y")


"""
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 0)
pd.set_option("display.max_colwidth", None)
"""

print(df)
