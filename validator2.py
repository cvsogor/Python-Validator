import itertools
import sys
import numpy as np
import pandas as pd

class DataValidator(object):
    def __init__(self, validators=None):
        self._validators = validators
        self._errors = []

    def validate(self, data):
        if self._validators:
            for validator in self._validators:
                try:
                    validator.validate(data)
                except Exception as ex:
                    self._errors.append(ex)
        return self._errors
       
class NanValidator(object):
    def __init__(self, check_cols_for_nan=None):
        self._cols = check_cols_for_nan

    def validate(self, df):
        if self._cols:
            if df[self._cols].isnull().any().any():
                raise TypeError("NaN values found")

class AccountTypeValidator(object):
    def __init__(self, column=None, expected_values=None):
        self._column = column        
        self._expected_values = expected_values

    def validate(self, df):
        if self._column and self._expected_values:
            actual = set(df[self._column].values) 
            expected = set(self._expected_values) 
            if not actual.issubset(expected):
                raise TypeError("Account type error")
                
class DuplicateValidator(object):
    def __init__(self, check_cols_for_duplicates=None):
        self._cols = check_cols_for_duplicates

    def validate(self, df):
        if self._cols:
            for col in self._cols:
                if df[col].duplicated().any():
                    raise ValueError("Duplicates found")
       
    
data_file = 'd:\Sources\Python Validation\data-dirty.xlsx'
#data_file = 'd:\Sources\Python Validation\data-clean.xlsx'
df = pd.read_excel(data_file, sheet_name='in')
df.rename(columns=lambda x: x.strip(), inplace=True)

    
nan_validator = NanValidator(["age", "account_type", "signup_date"])
account_type_validator = AccountTypeValidator("account_type", {"google", "facebook", "other"})      
duplicate_validator = DuplicateValidator(["guid", "age"])

validator = DataValidator([
                nan_validator,
                account_type_validator,       
                duplicate_validator])

errors = validator.validate(df)

if errors:
    print("Validation failed - {} errors found".format(len(errors)))
    for err in errors:
        print(err)
else:
    print("Validation complete")