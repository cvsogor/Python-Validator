import itertools
import sys
import numpy as np
import pandas as pd

data_file = 'd:\Sources\Python Validation\data-dirty.xlsx'
#data_file = 'd:\Sources\Python Validation\data-clean.xlsx'
df = pd.read_excel(data_file, sheet_name='in')
df.rename(columns=lambda x: x.strip(), inplace=True)
errors = []


check_cols_for_nan = ["age", "account_type", "signup_date"]
if df[check_cols_for_nan].isnull().any().any():
    errors.append("NaN values found")
        
actual = set(df["account_type"].values) 
expected = {"google", "facebook", "other"} 
if not actual.issubset(expected):
    errors.append("Account type error")

check_cols_for_duplicates = ["guid", "age"]
for col in check_cols_for_duplicates:
    if df[col].duplicated().any():
        errors.append("Duplicate rows found")
        break


if errors:
    print("Validation failed - {} errors found".format(len(errors)))
    for err in errors:
        print(err)
else:
    print("Validation complete")
