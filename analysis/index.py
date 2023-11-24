import pandas as pd
from footballmanager.analysis.domains import (
    base_meta_info,
    attributes
)

# Example Attribute/Stat Interface
speed_index = {
    # Col Name : weight
    'Pac':1,
    'Acc':1
}

work_index = {
    'Wor':1,
    'Sta':1,
}

set_piece_index = {
    'Jum':1,
    'Bra':1
}

class FMIndex:
    def __init__(
            self, 
            weighting_dict: dict = None, 
            name: str = None,
        ):
        self.weighting_dict = weighting_dict
        
        if name is None:
            self.name = 'index'
        else:
            self.name = name

    def compute(
            self, 
            data,
            keep_intermediates: bool = False,
            keep_meta: bool = True,
            keep_specific_cols: list = [],
            weight_scores: bool = True,
        ):
        for key in self.weighting_dict:
            assert key in data.columns, f"{key} column not found in data"

        # Handle data imputing here or in loop!
        additional_columns = []
        
        index_score = pd.Series([0]*len(data))
        weight = index_score.copy()
        for col in self.weighting_dict:
            # This would be removal method of handling missing data
            weight = weight + (~data[col].isna() * self.weighting_dict[col])
            intermediate = (data[col].fillna(0) * self.weighting_dict[col])
            if keep_intermediates:
                intermediate.name = f"{col}_intermediate"
                additional_columns.append(intermediate)

            index_score = index_score + intermediate
        
        if weight_scores:
            final = index_score / weight
        else:
            final = index_score
        
        final.name = self.name
        additional_columns.append(final)

        if keep_meta:
            col_intersection = list(set(data.columns) & set(base_meta_info+keep_specific_cols))
            data = pd.concat([data[col_intersection]] + additional_columns, axis=1)
        else:
            data = pd.concat([data] + additional_columns, axis=1)

        return data.sort_values(self.name, ascending=False)

attributes_index = FMIndex(name = "attributes_index", weighting_dict = {
    att:1 for att in attributes
})

gk_index = FMIndex(name = "gk_index", weighting_dict = {
    'Aer':60,
    'Cmd':40,
    'Com':30,
    'Ecc':20,
    'Fir':30,
    'Han':50,
    'Kic':35,
    '1v1':45,
    'Pas':45,
    # 'Pun':0
    'Ref':80,
    'TRO':40,
    'Thr':30,
    'Agg':40,
    'Ant':40,
    'Bra':30,
    'Cmp':40,
    'Cnt':65,
    'Dec':50,
    'Det':20,
    'Fla':20,
    'Ldr':10,
    # 'OtB':0,
    'Pos':40,
    'Ldr':10,
    'Vis':40,
    'Wor':10,
    'Acc':70,
    'Agi':100,
    'Bal':20,
    'Jum':45,
    'Nat':10,
    'Pac':50,
    'Sta':10,
    'Str':70,
    # Weak Foot
})

fb_index = FMIndex(name = "fb_index", weighting_dict={
    'Wor':5,
    'Acc':5,
    'Pac':5,
    'Sta':5,
    'Cro':3,
    'Dri':3,
    'Mar':3,
    'OtB':3,
    'Tck':3,
    'Tea':3,
    'Agi':1,
    'Ant':1,
    'Cnt':1,
    'Dec':1,
    'Fir':1,
    'Pas':1,
    'Pos':1,
    'Tec':1
})

