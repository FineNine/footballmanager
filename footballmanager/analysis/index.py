import pandas as pd
# Index class for taking dictionaries of attributes and their
# corresponding weights and computing a index/score
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
            data : pd.DataFrame,
            scale_weights: bool = False,
            keep_top_intermediates: bool = True,
            keep_all_intermediates: bool = False
    ):
        for key in self.weighting_dict:
            assert key in data.columns, f"{key} column not found in data"

        report_columns = []
        total_weighting = pd.Series([0]*len(data))
        total_score = total_weighting.copy()

        for element_name in self.weighting_dict:
            element = self.weighting_dict[element_name]

            if type(element) == int or type(element) == float:

                total_weighting += (~data[element_name].isna() * element)
                total_score += (data[element_name].fillna(0) * element) # How to handle missing data (this is effectively getting 0 score) add more imputation methods here


            if type(element) == dict:
                
                # form intermediate index
                intermediate_index = FMIndex(
                    name = element_name,
                    weighting_dict = element
                )

                # compute intermediate index
                intermediate_data = intermediate_index.compute(
                    data,
                    scale_weights=scale_weights,
                    keep_top_intermediates=keep_all_intermediates, # pursposeful, will cascade down if all is true
                    keep_all_intermediates=keep_all_intermediates
                )

                # add columns to report
                if keep_all_intermediates:
                    report_columns.append([intermediate_data[col] for col in intermediate_data])
                elif keep_top_intermediates:
                    report_columns.append(intermediate_data)

                # add weights
                total_weighting += sum([weight for ])

                # add to score
                total


# PreBuilt Indexes
PlayerAll = FMIndex(name = "")
