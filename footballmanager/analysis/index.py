import pandas as pd
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

    def compute(
            self,
            data : pd.DataFrame,
            scale_weights: bool = False,
            keep_all_indexes: bool = True,
    ):
        # for key in self.weighting_dict: how to programtically check all non dict value keys recursively to check column avail up front, not worth effort right now
        #     assert key in data.columns, f"{key} column not found in data"
        
        # Init Recursive Index Calculation
        self.data = data
        score, weight = self._compute_weighting_dict(
            self.weighting_dict,
            keep_all_indexes,
        )

        self.data[self.name] = score / weight

        return data
        
    def _compute_weighting_dict(
            self, 
            weighting_dict: dict, 
            keep_all_indexes: bool,
        ):
        score = 0
        weight = 0
        for key, value in weighting_dict.items():

            data_type = type(value)
            if data_type == dict:
                temp_score, temp_weight = self._compute_weighting_dict(value, keep_all_indexes)
                if keep_all_indexes:
                    self.data[key] = temp_score / temp_weight 
            elif data_type == float or data_type == int:
                temp_weight = value
                temp_score = self.data[key] * temp_weight
            else:
                raise TypeError
            
            score += temp_score
            weight += temp_weight
        return score, weight

# PreBuilt Indexes
PlayerAll = FMIndex(name = "")
