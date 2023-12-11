import pandas as pd
from typing import Any
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

    def __add__(self, other: Any):
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
            keep_only_relevant: bool = True,
    ):
        # for key in self.weighting_dict: how to programtically check all non dict value keys recursively to check column avail up front, not worth effort right now
        #     assert key in data.columns, f"{key} column not found in data"
        
        # Init Recursive Index Calculation
        _ = data.copy()
        self.data = data.copy()
        self.cols_used = []


        score, weight, index_list = self._compute_weighting_dict(
            self.weighting_dict,
            keep_all_indexes,
        )

        self.cols_used = basic_info + self.cols_used + index_list + [self.name]

        self.data[self.name] = score / weight

        # FORMATTING
        if keep_only_relevant:
            columns = [col for col in self.cols_used if col in self.data.columns]
            self.data = self.data[columns].copy()
        
        if sort:
            self.data.sort_values(by=self.name, ascending=sort_ascending, inplace=True, axis=0)

        return self.data
        
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
MobilityIndex = FMIndex(name = "Mobility", weighting_dict={
    'Acc':10,
    'Agi':10,
    'Pac':10,
})

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

SweeperKeeper = FMIndex(name = "SK", weighting_dict={
    'SK Essentials': {
        'Cmd':10,
        'Kic':10,
        '1v1':10,
        'Ref':10,
        'TRO':10,
        'Ant':10,
        'Cmp':10,
        'Cnt':10,
        'Pos':10,
        'Agi':10,
    },
    'SK Secondary': {
        'Aer':5,
        'Com':5,
        'Ecc':5,
        'Fir':5,
        'Han':5,
        'Pas':5,
        'Thr':5,
        'Dec':5,
        'Vis':5,
        'Acc':5,
    }
})

# Defenders
WideCenterBack = FMIndex(name = "BPD", weighting_dict={
    'BPD Essentials': {
        'Hea':10,
        'Mar':10,
        'Tck':10,
        'Pos':10,
        'Jum':10,
        'Str':10,
    },
    'BPD Secondary': {
        'Dri':5,
        'Fir':5,
        'Pas':5,
        'Tec':5,
        'Agg':5,
        'Ant':5,
        'Bra':5,
        'Cmp':5,
        'Cnt':5,
        'Dec':5,
        'Wor':5,
        'Agi':5,
        'Pac':5,
    }
})

# Full/Wing Backs
WingBack = FMIndex(name = "WB", weighting_dict={
    'WB Essentials': {
        'Cro':10,
        'Dri':10,
        'Mar':10,
        'Tck':10,
        'OtB':10,
        'Tea':10,
        'Wor':10,
        'Acc':10,
        'Sta':10,
    },
    'WB Secondary': {
        'Fir':5,
        'Pas':5,
        'Tec':5,
        'Ant':5,
        'Cnt':5,
        'Dec':5,
        'Pos':5,
        'Agi':5,
        'Bal':5,
        'Pac':5,
    }
})


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
TargetForward = FMIndex(name = "TF", weighting_dict={
    'TF Essentials': {
        'Fin':10,
        'Hea':10,
        'Bra':10,
        'Cmp':10,
        'OtB':10,
        'Bal':10,
        'Jum':10,
        'Str':10,
    },
    'TF Secondary': {
        'Fir':5,
        'Agg':5,
        'Ant':5,
        'Dec':5,
        'Tea':5,
    }
})

Poacher = FMIndex(name = 'Poacher', weighting_dict={
    'Poacher Essentials': {
        'Fin':10,
        'Ant':10,
        'Cmp':10,
        'OtB':10,
    },
    'Poacher Secondary': {
        'Fir':5,
        'Hea':5,
        'Tec':5,
        'Dec':5,
        'Acc':5,
    }
})
