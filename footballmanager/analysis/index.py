import pandas as pd
from footballmanager.analysis.domains import (
    basic_info,
    attributes,
    technicals,
    mentals,
    physicals,
    goalkeeping
)

# Index class for taking dictionaries of attributes and their
# corresponding weights and computing a index/score
class FMIndex:
    def __init__(
            self, 
            name: str = None,
            weighting_dict: dict = None, 
        ):
        self.weighting_dict = weighting_dict
        
        if name is None:
            self.name = 'index'
        else:
            self.name = name

    def __add__(self, other: 'FMIndex' | dict):
        if type(other) == type(self):
            for key, value in other.weighting_dict.items():
                self.weighting_dict[key] = value
        elif type(other) == dict:
            for key, value in other.items():
                self.weighting_dict[key] = value
        else:
            raise TypeError()
        

    def compute(
            self,
            data : pd.DataFrame,
            keep_all_indexes: bool = True,
            sort: bool = True,
            sort_ascending: bool = False,
            keep_only_relevant: bool = False,
    ):
        # for key in self.weighting_dict: how to programtically check all non dict value keys recursively to check column avail up front, not worth effort right now
        #     assert key in data.columns, f"{key} column not found in data"
        
        # Init Recursive Index Calculation
        self.data = data
        self.cols_used = []


        score, weight, index_list = self._compute_weighting_dict(
            self.weighting_dict,
            keep_all_indexes,
        )

        self.cols_used = basic_info + self.cols_used + index_list + [self.name]

        self.data[self.name] = score / weight

        # FORMATTING
        if keep_only_relevant:
            columns = [col for col in self.cols_used if col in data.columns]
            self.data = self.data[columns].copy()
        
        if sort:
            self.data.sort_values(by=self.name, ascending=sort_ascending, inplace=True, axis=0)

        return self.data.copy()
        
    def _compute_weighting_dict(
            self, 
            weighting_dict: dict, 
            keep_all_indexes: bool,
            index_list: list = []
        ):
        score = 0
        weight = 0

        for key, value in weighting_dict.items():

            data_type = type(value)
            if data_type == dict:
                temp_score, temp_weight, index_list = self._compute_weighting_dict(value, keep_all_indexes)
                if keep_all_indexes:
                    index_list.append(key)
                    self.data[key] = temp_score / temp_weight
            elif data_type == float or data_type == int:
                self.cols_used.append(key)
                temp_weight = value
                temp_score = self.data[key] * temp_weight
            else:
                raise TypeError
            
            score += temp_score
            weight += temp_weight
        return score, weight, index_list

### PreBuilt Indexes
## Classes of Att
TechnicalAttributeIndex = FMIndex(name = "Technical Att Index", weighting_dict={
    att:1 for att in technicals
})

MentalAttributeIndex = FMIndex(name = "Technical Att Index", weighting_dict={
    att:1 for att in mentals
})

PhysicalAttributeIndex = FMIndex(name = "Technical Att Index", weighting_dict={
    att:1 for att in physicals
})

GoalkeepingAttributeIndex = FMIndex(name = "Technical Att Index", weighting_dict={
    att:1 for att in goalkeeping
})

OutfieldPlayerAttributeIndex = FMIndex(name = "All Att Index", weighting_dict={
    "Technical":TechnicalAttributeIndex,
    "Mental":MentalAttributeIndex,
    "Phyiscal":PhysicalAttributeIndex
})



# GK

# Defenders

# Full/Wing Backs

# DM/CMs
BallWinningMidfielder = FMIndex(name="BWM", weighting_dict={
    'BWM Essentials': {
        'Tck':10,
        'Agg':10,
        'Ant':10,
        'Tea':10,
        'Wor':10,
        'Sta':10
    },
    'BWM Secondary': {
        'Mar':5,
        'Bra':5,
        'Cnt':5,
        'Pos':5,
        'Agi':5,
        'Pac':5,
        'Str':5
    },
})

# AMs

# WM/Wingers/Wide Forwards

# # Strikers

