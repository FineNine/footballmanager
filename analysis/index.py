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

gk_essential_index = {
    'Agi':1,
    'Ref':5, # total weighting of 6, reflexes get 5x weight
}

gk_core_index = {
    '1v1':1,
    'Ant':1,
    'Cmd':1,
    'Cnt':1,
    'Kic':1,
    'Pos':2,
}

gk_secondary_index = {
    'Acc':1,
    'Aer':1,
    'Cmp':1,
    'Dec':1,
    'Fir':1,
    'Han':1,
    'Pas':1,
    'Thr':1,
    'Vis':1,
}

# gk_index = gk_essential_index + gk_core_index + gk_secondary_index

class FMIndex:
    def __init__(
            self, 
            index: dict, 
            name: str = None,
            keep_intermediates: bool = False
        ):
        self.index = index
        self.keep_intermediates = keep_intermediates
        
        if name is None:
            self.name = 'index'
        else:
            self.name = name

    def compute(
            self, 
            data
        ):
        for key in self.index:
            assert key in data.columns, f"{key} column not found in data"

        # Handle data imputing here or in loop!
        
        index_score = pd.Series([0]*len(data))
        weight = index.copy()
        for col in self.index:
            # This would be removal method of handling missing data
            weight = weight + (~data[col].isna() * self.index[col])
            intermediate = (data[col].fillna(0) * self.index[col])
            if self.keep_intermediates:
                data[col+"_intermediate"] = intermediate
            index_score = index_score + intermediate
            
        data[self.name] = index_score