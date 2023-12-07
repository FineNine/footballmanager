import getpass
import os
import glob
import re
import pandas as pd
from pathlib import WindowsPath
from io import StringIO
from datetime import datetime
from typing import Tuple

# Parsers
def get_digits(val: str) -> float:
    return float(re.search(r'[+-]?([0-9]*[.])?[0-9]+', val.replace(',','')).group())

def parse_percent(val: str) -> float:
    # if val == '-':
        # return None
    # if pd.isnull(val) or val == 'nan':
    #     return None
    return float(val[:-1])/100

def parse_value(val: str) -> float:
    try:
        if '-' == val:
            return 0.

        # print(val, type(val))
        digits = get_digits(val)
        if 'M' in val:
            return digits * 1000000
        if 'K' in val:
            return digits * 1000
        else:
            return digits
    except:
        if pd.isnull(val) or val == 'nan' or val == "N/A" or val == '':
            return None
        
        raise ValueError

def parse_transfer_value(val: str) -> Tuple | None:
    min_value = None
    max_value = None
    if ' - ' in val:
        mini, maxi = val.split(' - ')
        min_value = parse_value(mini)
        max_value = parse_value(maxi)
    return min_value, max_value

def parse_wage(val: str) -> float | None:
    # Annualize wage value
    if '-' == val:
        return None
    if pd.isnull(val) or val == 'nan' or val == 'N/A':
        return None
    return get_digits(val)

    return

def parse_date(val: str) -> datetime | None: 
    # use re sub to remove parenthese if there is one
    if val == '-' or val == 'nan' or pd.isnull(val):
        return None
    return pd.to_datetime(val)

def parse_date_range(val: str) -> Tuple:
    if val == '-':
        return None, None
    if pd.isnull(val) or val == 'nan':
        return None, None
    if ' - ' in val:
        begin, end = val.split(' - ')
        begin_date = parse_date(begin)
        end_date = parse_date(end)
        return begin_date, end_date
    return None, None

def parse_dob(val: str) -> datetime:
    date = val.split('(')[0].strip()
    return parse_date(date)

def parse_distance(val: str) -> float | None:
    if val == '-':
        return None
    if pd.isnull(val) or val == 'nan':
        return None
    return get_digits(val)

def parse_weight(val: str) -> float | None:
    try:
        return get_digits(val)
    except:
        return None

def parse_height(val: str) -> float | None:
    if pd.isnull(val) or val == 'nan':
        return None
    if "'" in val and '"' in val:
        val = val.replace('"','')
        feet, inch = val.split("'")
        return int(feet)+(int(inch)/100)
    elif 'm' in val or 'cm' in val:
        return get_digits(val)
    return None

def parse_appearances(val: str) -> Tuple:
    if '-' == val:
        return None, None
    if pd.isnull(val) or val == 'nan':
        return None, None
    val = val.replace(')','')
    starts = None
    subs = None
    start_sub = val.split('(')
    if len(start_sub) == 2:
        starts = int(start_sub[0].strip())
        subs = int(start_sub[1].strip())
    else:
        starts = int(start_sub[0].strip())
    return starts, subs


# STATIC VARS
_OS_USERNAME = getpass.getuser()
DEFAULT_SI_REPO = f'C:/Users/{_OS_USERNAME}/Documents/Sports Interactive/Football Manager 2024/'
DEFAULT_COLUMN_CONVERTERS = {
    'Yearly Salary Raise': parse_percent,
    'Yearly Salary Raise':parse_percent,
    'Top Div Rel Salary Drop':parse_percent,
    'Top Div Prom Salary Raise':parse_percent,
    'Sell On Fee % Profit':parse_percent,
    'Sell On Fee %':parse_percent,
    'Rel Salary Drop':parse_percent,
    'Prom Salary Raise':parse_percent,
    '% Payroll/Sponsor':parse_percent,
    '% Gt. Receipts':parse_percent,
    '% Comp for Mgr Role':parse_percent,
    'Tck R':parse_percent,
    'Shot %':parse_percent,
    'Sv %':parse_percent,
    'Pas %':parse_percent,
    'OP-Cr %':parse_percent,
    'Hdr %':parse_percent,
    'xSv %':parse_percent,
    'Cr C/A':parse_percent,
    'Conv %':parse_percent,
    'Pen/R':parse_percent,
    'Gwin':parse_percent,
    'Unused Sub Fee':parse_value,
    'Act Non Prom Rls Fee':parse_value,
    'Top Score Bonus':parse_value,
    'Team Year Bonus':parse_value,
    'Shutout Bonus':parse_value,
    'SLGB (Gls)':parse_value,
    'SLGB':parse_value,
    'SLGAB':parse_value,
    'SLAB':parse_value,
    'Relegation Release':parse_value,
    'Min Fee Rls to Foreign Clubs':parse_value,
    'Min Fee Rls to Domestic Clubs':parse_value,
    'Min Fee Rls to Higher Div':parse_value,
    'Min Fee Rls Clubs Mjr Cont Comp':parse_value,
    'Min Fee Rls Clubs Cont Comp':parse_value,
    'Min Fee Rls':parse_value,
    'Int Cap Bonus':parse_value,
    'Goal Bonus':parse_value,
    'Committee Min Fee Rls':parse_value,
    'Assist Bonus':parse_value,
    'Appearance Fee':parse_value,
    'Act Rel Fee Rls':parse_value,
    'Min AP':parse_value,
    'Max AP':parse_value,
    'Scouting Cost':parse_value,
    'Transfer Fees Received':parse_value,
    'Last Trans. Fee':parse_value,
    'Transfer Value':parse_transfer_value,
    'New Wage':parse_wage,
    'Salary Contrib.':parse_wage,
    'Pot. Cap Impact':parse_wage,
    'Cap Impact':parse_wage,
    'Salary After Tax':parse_wage,
    'Salary':parse_wage,
    'Min WD':parse_wage,
    'Max WD':parse_wage,
    'Min Fee Rls to Foreign Clubs Exp':parse_date,
    'Min Fee Rls to Domestic Clubs Exp':parse_date,
    'Min Fee Rls to Higher Div Exp':parse_date,
    'Decrease Date':parse_date,
    'Min Fee Rls Clubs Mjr Cont Comp Exp':parse_date,
    'Min Fee Rls Clubs Cont Comp Exp':parse_date,
    'Min Fee Rls Clubs In Cont Comp Exp':parse_date,
    'Min Fee Rls Clubs In Cont Comp':parse_date,
    'Min Fee Rls Exp':parse_date,
    'Loan Duration':parse_date_range,
    'Loan Expires':parse_date,
    'New Date':parse_date,
    'Begins':parse_date,
    'Expires':parse_date,
    'Injured On':parse_date,
    'DOB':parse_dob,
    'Dist/90':parse_distance,
    'Distance':parse_distance,
    'Weight':parse_weight, # units need hyper param, everything does
    'Apps':parse_appearances,
    'Height':parse_height,
}

# Loading Export Functions
def parse_html_file(export_filepath: str = None) -> pd.DataFrame:
    file = open(os.path.abspath(export_filepath), 'r', encoding='utf-8')
    return pd.read_html(
        file, 
        flavor='bs4', 
        header=0, 
        encoding='utf-8', 
        na_values=["-"],
        converters=DEFAULT_COLUMN_CONVERTERS
    )[0]

def find_latest_file(dir: WindowsPath | str = DEFAULT_SI_REPO) -> str:
    list_of_files = glob.glob(os.path.join(dir, '*'))
    print(dir)
    print(list_of_files)
    return str(max(list_of_files, key=os.path.getctime))

def load_export(export_filepath: str = None) -> pd.DataFrame:
    if '.html' not in export_filepath:
        raise ValueError("File Specified not a valid file type (html), this may not be the latest file in the dir if using the 'find_latest_file'")

    # Passed to pandas for bs4 parsing html, if impl any other file types, then this must become a case statement
    data = parse_html_file(export_filepath)    
    data.columns = [re.split('\.\d', col_name, maxsplit=0)[0] for col_name in data.columns]

    return data