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
    'Cor':30,
    'Cro':25,
    'Dri':50,
    'Fin':10,
    'Fir':30,
    'Fre':10,
    'Hea':20,
    'Lon':10,
    'L Th':30,
    'Mar':45,
    'Pas':45,
    'Pen':10,
    'Tck':50,
    'Tec':45,
    'Agg':45,
    'Ant':45,
    'Bra':20,
    'Cmp':30,
    'Cnt':45,
    'Dec':45,
    'Det':20,
    'Fla':20,
    'Ldr':10,
    'OtB':70,
    'Pos':30,
    'Tea':10,
    'Vis':25,
    'Wor':90,
    'Acc':100,
    'Agi':60,
    'Bal':25,
    'Jum':40,
    'Nat':10,
    'Pac':90,
    'Sta':100,
    'Str':25,
    # weak foot
})

cb_index = FMIndex(name = 'cb_index', weighting_dict = {
    'Cor':5,
    'Cro':20,
    'Dri':40,
    'Fin':10,
    'Fir':35,
    'Fre':10,
    'Hea':55,
    'Lon':10,
    'L Th':5,
    'Mar':55,
    'Pas':55,
    'Pen':10,
    'Tck':40,
    'Tec':35,
    'Agg':40,
    'Ant':50,
    'Bra':30,
    'Cmp':80,
    'Cnt':50,
    'Dec':50,
    'Det':20,
    'Fla':10,
    'Ldr':10,
    'OtB':10,
    'Pos':55,
    'Tea':10,
    'Vis':50,
    'Wor':55,
    'Acc':90,
    'Agi':60,
    'Bal':35,
    'Jum':65,
    'Nat':10,
    'Pac':90,
    'Sta':30,
    'Str':50,
})

cm_index = FMIndex(name = "cm_index", weighting_dict = {
    'Cor':10,
    'Cro':10,
    'Dri':45,
    'Fin':20,
    'Fir':50,
    'Fre':30,
    'Hea':10,
    'Lon':40,
    'L Th':5,
    'Mar':20,
    'Pas':65,
    'Pen':10,
    'Tck':35,
    'Tec':50,
    'Agg':50,
    'Ant':55,
    'Bra':30,
    'Cmp':60,
    'Cnt':50,
    'Dec':65,
    'Det':20,
    'Fla':50,
    'Ldr':10,
    'OtB':40,
    'Pos':65,
    'Tea':10,
    'Vis':55,
    'Wor':90,
    'Acc':65,
    'Agi':45,
    'Bal':35,
    'Jum':15,
    'Nat':10,
    'Pac':70,
    'Sta':70,
    'Str':35,
    # Weak Foot
})

cm_index = FMIndex(name = "cm_index", weighting_dict = {
    'Cor':10,
    'Cro':10,
    'Dri':45,
    'Fin':20,
    'Fir':50,
    'Fre':30,
    'Hea':10,
    'Lon':40,
    'L Th':5,
    'Mar':20,
    'Pas':65,
    'Pen':10,
    'Tck':35,
    'Tec':50,
    'Agg':50,
    'Ant':55,
    'Bra':30,
    'Cmp':60,
    'Cnt':50,
    'Dec':65,
    'Det':20,
    'Fla':50,
    'Ldr':10,
    'OtB':40,
    'Pos':65,
    'Tea':10,
    'Vis':55,
    'Wor':90,
    'Acc':65,
    'Agi':45,
    'Bal':35,
    'Jum':15,
    'Nat':10,
    'Pac':70,
    'Sta':70,
    'Str':35,
    # Weak Foot
})

am_index = FMIndex(name = "am_index", weighting_dict = {
    'Cor':5,
    'Cro':5,
    'Dri':65,
    'Fin':65,
    'Fir':40,
    'Fre':30,
    'Hea':10,
    'Lon':20,
    'L Th':1,
    'Mar':5,
    'Pas':50,
    'Pen':15,
    'Tck':15,
    'Tec':65,
    'Agg':50,
    'Ant':70,
    'Bra':20,
    'Cmp':35,
    'Cnt':25,
    'Dec':40,
    'Det':20,
    'Fla':20,
    'Ldr':10,
    'OtB':35,
    'Pos':10,
    'Tea':10,
    'Vis':30,
    'Wor':80,
    'Acc':100,
    'Agi':30,
    'Bal':50,
    'Jum':10,
    'Nat':10,
    'Pac':80,
    'Sta':80,
    'Str':30,
    # Weak Foot
})

st_index = FMIndex(name = "st_index", weighting_dict = {
    'Cor':5,
    'Cro':5,
    'Dri':75,
    'Fin':80,
    'Fir':50,
    'Fre':5,
    'Hea':25,
    'Lon':25,
    'L Th':1,
    'Mar':1,
    'Pas':40,
    'Pen':20,
    'Tck':5,
    'Tec':65,
    'Agg':50,
    'Ant':50,
    'Bra':20,
    'Cmp':35,
    'Cnt':5,
    'Dec':45,
    'Det':20,
    'Fla':25,
    'Ldr':10,
    'OtB':45,
    'Pos':5,
    'Tea':10,
    'Vis':20,
    'Wor':60,
    'Acc':100,
    'Agi':30,
    'Bal':50,
    'Jum':20,
    'Nat':10,
    'Pac':70,
    'Sta':65,
    'Str':25,
    # Weak Foot
})

