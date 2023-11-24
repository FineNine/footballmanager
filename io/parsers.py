import pandas as pd
import re
from datetime import datetime
from typing import Tuple, Union

# TODO
# Make class for unit switch
# Finish Wage
# Optimize control flow of parsers

def get_digits(val: str) -> float:
    return float(re.search(r'[+-]?([0-9]*[.])?[0-9]+', val.replace(',','')).group())

def parse_value(val: str) -> Union[float, None]:
    if '-' == val:
        return 0.
    if pd.isnull(val) or val == 'nan':
        return None
    digits = get_digits(val)
    if 'M' in val:
        return digits * 1000000
    if 'K' in val:
        return digits * 1000
    else:
        return digits

def parse_transfer_value(val: str) -> Union[Tuple, None]:
    min_value = None
    max_value = None
    if ' - ' in val:
        mini, maxi = val.split(' - ')
        min_value = parse_value(mini)
        max_value = parse_value(maxi)
    return min_value, max_value

def parse_percent(val: str) -> Union[float, None]:
    if val == '-':
        return None
    if pd.isnull(val) or val == 'nan':
        return None
    return float(val[:-1])/100

def parse_wage(val: str) -> Union[float, None]:
    # Annualize wage value
    if '-' == val:
        return None
    if pd.isnull(val) or val == 'nan':
        return None
    return get_digits(val)

    return

def parse_date(val: str) -> Union[datetime, None]: 
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

def parse_nulled_int(val: str) -> Union[Tuple, int, None]:
    # dash (-) equals 0, frustrating that you even have to parse
    if val == '-':
        return None
    if pd.isnull(val) or val == 'nan':
        return None
    if ' - ' in val:
        lower, upper = val.split(' - ')
        return int(lower), int(upper)
    return int(val)

def parse_nulled_float(val: str) -> Union[Tuple, float, None]:
    if val == '-':
        return None
    if pd.isnull(val) or val == 'nan':
        return None
    if ' - ' in val:
        lower, upper = val.split(' - ')
        return float(lower), float(upper)
    return float(val)

def parse_distance(val: str) -> Union[float, None]:
    if val == '-':
        return None
    if pd.isnull(val) or val == 'nan':
        return None
    return get_digits(val)

def parse_weight(val: str) -> Union[float, None]:
    try:
        return get_digits(val)
    except:
        return None

def parse_height(val: str) -> Union[float, None]:
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
    starts, subs = val.split('(')
    return int(starts.strip()), int(subs)

parse_mapping = {
    # A commented column field indicates no parsing needed, just want documentation
    # Information
    # Name
    # Ability (drop)
    # Role Ability (drop)
    # Potential (drop)
    # Attributes (only format as int)
# Info
    'Inf':None,
    'Name':None,

# Attribute
    '1v1':parse_nulled_int,
    'Acc':parse_nulled_int,
    'Aer':parse_nulled_int,
    'Agg':parse_nulled_int,
    'Agi':parse_nulled_int,
    'Ant':parse_nulled_int,
    'Bal':parse_nulled_int,
    'Bra':parse_nulled_int,
    'Cmd':parse_nulled_int,
    'Cnt':parse_nulled_int,
    'Cmp':parse_nulled_int,
    'Cro':parse_nulled_int,
    'Dec':parse_nulled_int,
    'Det':parse_nulled_int,
    'Dri':parse_nulled_int,
    'Fin':parse_nulled_int,
    'Fir':parse_nulled_int,
    'Fla':parse_nulled_int,
    'Han':parse_nulled_int,
    'Hea':parse_nulled_int,
    'Jum':parse_nulled_int,
    'Kic':parse_nulled_int,
    'Ldr':parse_nulled_int,
    'Lon':parse_nulled_int,
    'L Th':parse_nulled_int,
    'Fre':parse_nulled_int,
    'Mar':parse_nulled_int,
    'OtB':parse_nulled_int,
    'Pac':parse_nulled_int,
    'Pas':parse_nulled_int,
    'Pos':parse_nulled_int,
    'Ref':parse_nulled_int,
    'Pun':parse_nulled_int,
    'Pen':parse_nulled_int,
    'Sta':parse_nulled_int,
    'Str':parse_nulled_int,
    'Tck':parse_nulled_int,
    'Tea':parse_nulled_int,
    'Tec':parse_nulled_int,
    'Thr':parse_nulled_int,
    'TRO':parse_nulled_int,
    'Vis':parse_nulled_int,
    'Wor':parse_nulled_int,
    'Cor':parse_nulled_int,
    'Ecc':parse_nulled_int,
    'Com':parse_nulled_int,
    
# Club
    'Based':None,
    'Division':None,
    'Club':None,

# Coaching
    'Best Pos':None,
    'Style':None,
    'Best Role':None, # we take the full name
    'Best Duty':None,

# Contract
    'Act Non Prom Rls Fee':parse_value,
    'Non Prom Rls Cls':None,
    'Yearly Salary Raise':parse_percent,
    'New Wage':parse_wage,
    'Unused Sub Fee':parse_value,
    'Transfer Options':None,
    'Top Score Bonus':parse_value,
    'Top Div Rel Salary Drop':parse_percent,
    'Top Div Prom Salary Raise':parse_percent,
    'Team Year Bonus':parse_value,
    'Offer Status':None,
    'Shutout Bonus':parse_value,
    'Release':None,
    'Sell On Fee % Profit':parse_percent,
    'Sell On Fee %':parse_percent,
    'SLGB (Gls)':parse_value,
    'SLGB':parse_value,
    'SLGAB':parse_value,
    'SLAB':parse_value,
    'Salary Contrib.':parse_wage,
    'Pot. Cap Impact':parse_wage,
    'Cap Impact':parse_wage,
    'Salary After Tax':parse_wage,
    'WaCLG':None,
    'Salary':parse_wage,
    'Rel Salary Drop':parse_percent,
    'Relegation Release':parse_value,
    'Prom Salary Raise':parse_percent,
    '% Payroll/Sponsor':parse_percent,
    '% Gt. Receipts':parse_percent,
    '% Comp for Mgr Role':parse_percent,
    'Player Rights':None,
    'Opt Ext by Club':None,
    '1 Year Ext Prom Aft Games':None,
    '1 Year Ext Aft Games':None,
    '1 Year Ext Rel Aft Games':None,
    'Non-Playing Rel':None,
    'Non-Prom Rls Cls':None,
    'Min Fee Rls to Foreign Clubs Exp':parse_date,
    'Min Fee Rls to Foreign Clubs':parse_value,
    'Min Fee Rls to Domestic Clubs Exp':parse_date,
    'Min Fee Rls to Domestic Clubs':parse_value,
    'Min Fee Rls to Higher Div Exp':parse_date,
    'Min Fee Rls to Higher Div':parse_value,
    'Decrease Date':parse_date,
    'Min Fee Rls Clubs Mjr Cont Comp Exp':parse_date,
    'Min Fee Rls Clubs Mjr Cont Comp':parse_value,
    'Min Fee Rls Clubs Cont Comp Exp':parse_date,
    'Min Fee Rls Clubs Cont Comp':parse_value,
    'Min Fee Rls Clubs In Cont Comp Exp':parse_date,
    'Min Fee Rls Clubs In Cont Comp':parse_date,
    'Min Fee Rls Exp':parse_date,
    'Min Fee Rls':parse_value,
    'Mtch High Earn':None,
    'Loan Duration':parse_date_range,
    'Loan Expires':parse_date,
    'Int Cap Bonus':parse_value,
    'Injury Rls':None,
    'G. Con':None,
    'Goal Bonus':parse_value,
    'F/PT':None,
    'FFP Contribution':None,
    'New Date':parse_date,
    'Type':None,
    'Begins':parse_date,
    'Extension After Promotion':None,
    'Expires':parse_date,
    'Committee Min Fee Rls':parse_value,
    'Assist Bonus':parse_value,
    'Appearance Fee':parse_value,
    'Act Rel Fee Rls':parse_value,
    
# Happiness/Dynamic
    'General Happiness':None,
    'Short-term Plans':None,
    'Morale':None,
    'Long-term Plans':None,
    'International Happiness':None,

# Injury/Fitness
    'Fatigue':None, # maybe time delta
    'Time Out':None,
    'Rc Injury':None,
    'CON':None,
    'Injury Risk':None,
    'NT Injury':None,
    'Injury':None,
    'Injured On':parse_date,

# General
    'Age':None,
    'Weight':parse_weight, # units need hyper param, everything does
    'UID':None,
    'No.':None,
    'Sec. Position':None,
    '2nd Nat':None,
    'Right Foot':None,
    'Birth Region':None,
    'Prom.':None,
    'Pref.':None, # dash meens prob have to parse
    'Preferred Foot':None,
    'Position':None,
    'Birth City':None,
    'Personality':None,
    'Nat':None,
    'NoB':None,
    'Media Handling':None,
    'Media Description':None,
    'Left Foot':None,
    'Home Grown Status':None,
    'Height':parse_height,
    'Favored Personnel':None,
    'Favored Clubs':None,
    'EU National':None,
    'Eligible':None,
    'Due Date':None,
    'Development Advice':None,
    'DOB':parse_dob,
    'Based In':None,


# International
    'Caps':None,
    'Yth Gls':parse_nulled_int,
    'Yth Apps':parse_nulled_int,
    'Team':None,
    'Goals':parse_nulled_int,

# Scouting 
    'Ability':None,
    'Cons':None,
    'Pros':None,
    'Style':None,
    'Min WD':parse_wage,
    'Min AP':parse_value,
    'Max WD':parse_wage,
    'Max AP':parse_value,
    'Best Role':None,
    'Best Duty':None,
    'Best Pos':None,
    'RF Matches':None,
    'Potential':None,
    'Days':None, # potentially parse out days if in value
    'Knowledge':None,
    'Days Old':None, # potentially parse out days if in value
    'Current Focuses':None,
    'Scouting Cost':parse_value,

# Squad
    'PI':None,
    'Suitability':None,
    'Tac Fami':None,
    'Playing Time':None,

# Stats Gen
    'Hdrs A':parse_nulled_int,
    'Tck/90':parse_nulled_float,
    'Tck W':parse_nulled_int,
    'Tck A':parse_nulled_int,
    'Tck R':parse_percent,
    'Shot/90':parse_nulled_float,
    'Shot %':parse_percent,
    'ShT/90':parse_nulled_float,
    'ShT':parse_nulled_int,
    'Shots Outside Box/90':parse_nulled_float,
    'Shts Blckd/90':parse_nulled_float,
    'Shts Blckd':parse_nulled_int,
    'Shots':parse_nulled_int,
    'Svt':parse_nulled_int,
    'Svp':parse_nulled_int,
    'Svh':parse_nulled_int,
    'Sv %':parse_percent,
    'Pr passes/90':parse_nulled_float,
    'Pr Passes':parse_nulled_int,
    'Pres C/90':parse_nulled_float,
    'Pres C':parse_nulled_int,
    'Pres A/90':parse_nulled_float,
    'Pres A':parse_nulled_int,
    'Poss Won/90':parse_nulled_float,
    'Poss Lost/90':parse_nulled_float,
    'Ps C/90':parse_nulled_float,
    'Ps C':parse_nulled_int,
    'Ps A/90':parse_nulled_float,
    'Pas A':parse_nulled_int,
    'Pas %':parse_percent,
    'OP-KP/90':parse_nulled_float,
    'OP-KP':parse_nulled_int,
    'OP-Crs C/90':parse_nulled_float,
    'OP-Crs C':parse_nulled_int,
    'OP-Crs A/90':parse_nulled_float,
    'OP-Crs A':parse_nulled_int,
    'OP-Cr %':parse_percent,
    'Off':parse_nulled_int,
    'Gl Mst':parse_nulled_int,
    'K Tck/90':parse_nulled_float,
    'K Tck':parse_nulled_int,
    'K Ps/90':parse_nulled_float,
    'K Pas':parse_nulled_int,
    'K Hdrs/90':parse_nulled_float,
    'Int/90':parse_nulled_float,
    'Itc':parse_nulled_int,
    'Sprints/90':parse_nulled_float,
    'Hdr %':parse_percent,
    'Hdrs W/90':parse_nulled_float,
    'Hdrs':parse_nulled_int,
    'Hdrs L/90':parse_nulled_float,
    'Goals Outside Box':parse_nulled_int,
    'FK Shots':parse_nulled_int,
    'xSv %':parse_percent,
    'xGP/90':parse_nulled_float,
    'xGP':parse_nulled_float,
    'xG/shot':parse_nulled_float,
    'Drb/90':parse_nulled_float,
    'Drb':parse_nulled_int,
    'Dist/90':parse_distance,
    'Distance':parse_distance,
    'Cr C/90':parse_nulled_float,
    'Cr C':parse_nulled_int,
    'Crs A/90':parse_nulled_float,
    'Cr A':parse_nulled_int,
    'Cr C/A':parse_percent,
    'Conv %':parse_percent,
    'Clr/90':parse_nulled_float,
    'Clear':parse_nulled_float,
    'CCC':parse_nulled_int,
    'Ch C/90':parse_nulled_float,
    'Blk/90':parse_nulled_float,
    'Blk':parse_nulled_int,
    'Asts/90':parse_nulled_float,
    'Aer A/90':parse_nulled_float,

# Stats Gen
    'AT Apps':parse_nulled_int,
    'Yel':parse_nulled_int,
    'xG':parse_nulled_float,
    'Saves/90':parse_nulled_float,
    'Tgls/90':parse_nulled_float,
    'Tcon/90':parse_nulled_float,
    'Tall':parse_nulled_int,
    'Tgls':parse_nulled_int,
    'Starts':parse_nulled_int,
    'Shutouts':parse_nulled_int,
    'Red':parse_nulled_int,
    'Pts/Gm':parse_nulled_float,
    'PoM':parse_nulled_int,
    'Pen/R':parse_percent,
    'Pens S':parse_nulled_int,
    'Pens Saved Ratio':None,
    'Pens Saved':parse_nulled_int,
    'Pens Faced':parse_nulled_int,
    'Pens':parse_nulled_int,
    'NP-xG/90':parse_nulled_float,
    'NP-xG':parse_nulled_float,
    'Last Gl':parse_nulled_float,
    'Last C':parse_nulled_float,
    'Mins/Gm':parse_nulled_float,
    'Mins':parse_nulled_int,
    'Last 5 Games':parse_nulled_float,
    'Last 5 FT Games':parse_nulled_float,
    'Int Conc':parse_nulled_int,
    'Int Av Rat':parse_nulled_float,
    'Int Ast':parse_nulled_int,
    'Int Apps':parse_nulled_int,
    'Gls/90':parse_nulled_float,
    'All/90':parse_nulled_float,
    'Conc':parse_nulled_int,
    'Gls':parse_nulled_int,
    'Won':parse_nulled_int,
    'G. Mis':parse_nulled_int,
    'Lost':parse_nulled_int,
    'D':parse_nulled_int,
    'Gwin':parse_percent,
    'Fls':parse_nulled_int,
    'FA':parse_nulled_int,
    'xG/90':parse_nulled_float,
    'xG-OP':parse_nulled_float,
    'xA/90':parse_nulled_float,
    'xA':parse_nulled_float,
    'Cln/90':parse_nulled_float,
    'Av Rat':parse_nulled_float,
    'Mins/Gl':parse_nulled_float,
    'Ast':parse_nulled_int,
    'Apps':parse_appearances,
    'AT Lge Gls':parse_nulled_int,
    'AT Lge Apps':parse_nulled_int,
    'AT Gls':parse_nulled_int,

# Training
    'Focus':None,
    'Workload':None,
    'Training Happiness Details':None,
    'Training Happiness':None,
    'PoTe':None,
    'PoTa':None,
    'Position/Role/Duty':None,
    'New Player Trait':None,
    'Performance':None,
    'Level':None,
    'GKS':None,
    'GKH':None,
    'Fit':None,
    'DeTe':None,
    'AtTa':None,

# Transfer
    'Actual Playing Time':None,
    'WP Needed':None,
    'WP Chance':None,
    'Type':None,
    'Transfer Value':parse_transfer_value,
    'Transfer Status':None,
    'Transfer Fees Received':parse_value,
    "Player's Interest":None,
    'Ovr':None,
    'On Loan From':None,
    'Loan Status':None,
    'Last Trans. Fee':parse_value,
    'Last Club':None,
    'Future Playing Time':None,
    'Fee':None,
    'Round':None,
    'Pick':None,
    'Drafted Club':None,
    'Season 2027/28':None, # create dictionary or something?
    'Season 2026/27':None, 
    'Season 2025/26':None,
    'Season 2024/25':None,
    'Asking Price':None,
    'Agreed Playing Time':None,
    'Agent':None, # we use the full name version

# Hidden    

# Drop List
    'Ability':None,
    'Role Ability':None,
    'Potential':None,
    'Will Leave At End Of Contract':None,
    'Will Explore Options At End Of Contract':None,
    'Waive Comp for Mgr Role':None,
    'SHP':None,
    'WR':None,
    'Recent Changes (Last 2 Weeks)':None,
}

drop_list = [
    'Ability',
    'Role Ability',
    'Potential',
    'Will Leave At End of Contract',
    'Will Explore Options At End Of Contract',
    'Waive Comp for Mgr Role',
    'SHP',
    'WR',
    'Recent Changes (Last 2 Weeks)'
]

# Type needed before parsing
type_mapping = {
# Info
    'Inf':str,
    'Name':str,

# Attribute
    '1v1':str,
    'Acc':str,
    'Aer':str,
    'Agg':str,
    'Agi':str,
    'Ant':str,
    'Bal':str,
    'Bra':str,
    'Cmd':str,
    'Cnt':str,
    'Cmp':str,
    'Cro':str,
    'Dec':str,
    'Det':str,
    'Dri':str,
    'Fin':str,
    'Fir':str,
    'Fla':str,
    'Han':str,
    'Hea':str,
    'Jum':str,
    'Kic':str,
    'Ldr':str,
    'Lon':str,
    'L Th':str,
    'Fre':str,
    'Mar':str,
    'OtB':str,
    'Pac':str,
    'Pas':str,
    'Pos':str,
    'Ref':str,
    'Pun':str,
    'Pen':str,
    'Sta':str,
    'Str':str,
    'Tck':str,
    'Tea':str,
    'Tec':str,
    'Thr':str,
    'TRO':str,
    'Vis':str,
    'Wor':str,
    'Cor':str,
    'Ecc':str,
    'Com':str,

# Club
    'Based':str,
    'Division':str,
    'Club':str,

# Coaching
    'Best Pos':str,
    'Style':str,
    'Best Role':str, # we take the full name
    'Best Duty':str,

# Contract
    'Act Non Prom Rls Fee':str,
    'Non Prom Rls Cls':str,
    'Yearly Salary Raise':str,
    'New Wage':str,
    'Unused Sub Fee':str,
    'Transfer Options':str,
    'Top Score Bonus':str,
    'Top Div Rel Salary Drop':str,
    'Top Div Prom Salary Raise':str,
    'Team Year Bonus':str,
    'Offer Status':str,
    'Shutout Bonus':str,
    'Release':str,
    'Sell On Fee % Profit':str,
    'Sell On Fee %':str,
    'SLGB (Gls)':str,
    'SLGB':str,
    'SLGAB':str,
    'SLAB':str,
    'Salary Contrib.':str,
    'Pot. Cap Impact':str,
    'Cap Impact':str,
    'Salary After Tax':str,
    'WaCLG':str,
    'Salary':str,
    'Rel Salary Drop':str,
    'Relegation Release':str,
    'Prom Salary Raise':str,
    '% Payroll/Sponsor':str,
    '% Gt. Receipts':str,
    '% Comp for Mgr Role':str,
    'Player Rights':str,
    'Opt Ext by Club':str,
    '1 Year Ext Prom Aft Games':str,
    '1 Year Ext Aft Games':str,
    '1 Year Ext Rel Aft Games':str,
    'Non-Playing Rel':str,
    'Non-Prom Rls Cls':str,
    'Min Fee Rls to Foreign Clubs Exp':str,
    'Min Fee Rls to Foreign Clubs':str,
    'Min Fee Rls to Domestic Clubs Exp':str,
    'Min Fee Rls to Domestic Clubs':str,
    'Min Fee Rls to Higher Div Exp':str,
    'Min Fee Rls to Higher Div':str,
    'Decrease Date':str,
    'Min Fee Rls Clubs Mjr Cont Comp Exp':str,
    'Min Fee Rls Clubs Mjr Cont Comp':str,
    'Min Fee Rls Clubs Cont Comp Exp':str,
    'Min Fee Rls Clubs Cont Comp':str,
    'Min Fee Rls Clubs In Cont Comp Exp':str,
    'Min Fee Rls Clubs In Cont Comp':str,
    'Min Fee Rls Exp':str,
    'Min Fee Rls':str,
    'Mtch High Earn':str,
    'Loan Duration':str,
    'Loan Expires':str,
    'Int Cap Bonus':str,
    'Injury Rls':str,
    'G. Con':bool,
    'Goal Bonus':str,
    'F/PT':str,
    'FFP Contribution':str,
    'New Date':str,
    'Type':str,
    'Begins':str,
    'Extension After Promotion':str,
    'Expires':str,
    'Committee Min Fee Rls':str,
    'Assist Bonus':str,
    'Appearance Fee':str,
    'Act Rel Fee Rls':str,

# Happiness/Dynamic
    'General Happiness':str,
    'Short-term Plans':str,
    'Morale':str,
    'Long-term Plans':str,
    'International Happiness':str,

# Injury/Fitness
    'Fatigue':str,
    'Time Out':str,
    'Rc Injury':str,
    'CON':str,
    'Injury Risk':str,
    'NT Injury':str,
    'Injury':str,
    'Injured On':str,

# General
    'Age':int,
    'Weight':str, # units need hyper param, everything does
    'UID':int,
    'No.':str,
    'Sec. Position':str,
    '2nd Nat':str,
    'Right Foot':str,
    'Birth Region':str,
    'Prom.':str,
    'Pref.':str, # dash meens prob have to parse
    'Preferred Foot':str,
    'Position':str,
    'Birth City':str,
    'Personality':str,
    'Nat':str,
    'NoB':str,
    'Media Handling':str,
    'Media Description':str,
    'Left Foot':str,
    'Home Grown Status':str,
    'Height':str,
    'Favored Personnel':str,
    'Favored Clubs':str,
    'EU National':bool,
    'Eligible':bool,
    'Due Date':str,
    'Development Advice':str,
    'DOB':str,
    'Based In':str,

# International
    'Caps':int,
    'Yth Gls':str,
    'Yth Apps':str,
    'Team':str,
    'Goals':str,

# Scouting 
    'Ability':str,
    'Cons':str,
    'Pros':str,
    'Style':str,
    'Min WD':str,
    'Min AP':str,
    'Max WD':str,
    'Max AP':str,
    'Best Role':str,
    'Best Duty':str,
    'Best Pos':str,
    'RF Matches':str,
    'Potential':str,
    'Days':str,
    'Knowledge':str,
    'Days Old':str,
    'Current Focuses':str,
    'Scouting Cost':str,

# Squad
    'PI':str,
    'Suitability':str,
    'Tac Fami':str,
    'Playing Time':str,

# Stats Gen
    'Hdrs A':str,
    'Tck/90':str,
    'Tck W':str,
    'Tck A':str,
    'Tck R':str,
    'Shot/90':str,
    'Shot %':str,
    'ShT/90':str,
    'ShT':str,
    'Shots Outside Box/90':str,
    'Shts Blckd/90':str,
    'Shts Blckd':str,
    'Shots':str,
    'Svt':str,
    'Svp':str,
    'Svh':str,
    'Sv %':str,
    'Pr passes/90':str,
    'Pr Passes':str,
    'Pres C/90':str,
    'Pres C':str,
    'Pres A/90':str,
    'Pres A':str,
    'Poss Won/90':str,
    'Poss Lost/90':str,
    'Ps C/90':str,
    'Ps C':str,
    'Ps A/90':str,
    'Pas A':str,
    'Pas %':str,
    'OP-KP/90':str,
    'OP-KP':str,
    'OP-Crs C/90':str,
    'OP-Crs C':str,
    'OP-Crs A/90':str,
    'OP-Crs A':str,
    'OP-Cr %':str,
    'Off':str,
    'Gl Mst':str,
    'K Tck/90':str,
    'K Tck':str,
    'K Ps/90':str,
    'K Pas':str,
    'K Hdrs/90':str,
    'Int/90':str,
    'Itc':str,
    'Sprints/90':str,
    'Hdr %':str,
    'Hdrs W/90':str,
    'Hdrs':str,
    'Hdrs L/90':str,
    'Goals Outside Box':str,
    'FK Shots':str,
    'xSv %':str,
    'xGP/90':str,
    'xGP':str,
    'xG/shot':str,
    'Drb/90':str,
    'Drb':str,
    'Dist/90':str,
    'Distance':str,
    'Cr C/90':str,
    'Cr C':str,
    'Crs A/90':str,
    'Cr A':str,
    'Cr C/A':str,
    'Conv %':str,
    'Clr/90':str,
    'Clear':str,
    'CCC':str,
    'Ch C/90':str,
    'Blk/90':str,
    'Blk':str,
    'Asts/90':str,
    'Aer A/90':str,

# Stats Gen
    'AT Apps':str,
    'Yel':str,
    'xG':str,
    'Saves/90':str,
    'Tgls/90':str,
    'Tcon/90':str,
    'Tall':str,
    'Tgls':str,
    'Starts':str,
    'Shutouts':str,
    'Red':str,
    'Pts/Gm':str,
    'PoM':str,
    'Pen/R':str,
    'Pens S':str,
    'Pens Saved Ratio':str,
    'Pens Saved':str,
    'Pens Faced':str,
    'Pens':str,
    'NP-xG/90':str,
    'NP-xG':str,
    'Last Gl':str,
    'Last C':str,
    'Mins/Gm':str,
    'Mins':str,
    'Last 5 Games':str,
    'Last 5 FT Games':str,
    'Int Conc':str,
    'Int Av Rat':str,
    'Int Ast':str,
    'Int Apps':str,
    'Gls/90':str,
    'All/90':str,
    'Conc':str,
    'Gls':str,
    'Won':str,
    'G. Mis':str,
    'Lost':str,
    'D':str,
    'Gwin':str,
    'Fls':str,
    'FA':str,
    'xG/90':str,
    'xG-OP':str,
    'xA/90':str,
    'xA':str,
    'Cln/90':str,
    'Av Rat':str,
    'Mins/Gl':str,
    'Ast':str,
    'Apps':str,
    'AT Lge Gls':str,
    'AT Lge Apps':str,
    'AT Gls':str,

# Training
    'Focus':str,
    'Workload':str,
    'Training Happiness Details':str,
    'Training Happiness':str,
    'PoTe':str,
    'PoTa':str,
    'Position/Role/Duty':str,
    'New Player Trait':str,
    'Performance':str,
    'Level':str,
    'GKS':str,
    'GKH':str,
    'Fit':str,
    'DeTe':str,
    'AtTa':str,

# Transfer
    'Actual Playing Time':str,
    'WP Needed':bool,
    'WP Chance':str,
    'Type':str,
    'Transfer Value':str,
    'Transfer Status':str,
    'Transfer Fees Received':str,
    "Player's Interest":str,
    'Ovr':str,
    'On Loan From':str,
    'Loan Status':str,
    'Last Trans. Fee':str,
    'Last Club':str,
    'Future Playing Time':str,
    'Fee':str,
    'Round':str,
    'Pick':str,
    'Drafted Club':str,
    'Season 2027/28':str, # create dictionary or something?
    'Season 2026/27':str, 
    'Season 2025/26':str,
    'Season 2024/25':str,
    'Asking Price':str,
    'Agreed Playing Time':str,
    'Agent':str, # we use the full name version

# Hidden

# Drop List
    'Ability':str,
    'Role Ability':str,
    'Potential':str,
    'Will Leave At End Of Contract':str,
    'Will Explore Options At End Of Contract':str,
    'Waive Comp for Mgr Role':str,
    'SHP':str,
    'WR':str,
    'Recent Changes (Last 2 Weeks)':str,
}