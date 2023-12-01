import pandas as pd
import re
import glob
import getpass
import os
from .tools import get_latest_file
from footballmanager.io.parsers import parse_mapping, type_mapping

# TODO
# print list of folders and files

class FMLoader():
    def __init__(self, data_dir: str = None):
        if data_dir is None:
            username = getpass.getuser()
            self.data_dir = f'C:/Users/{username}/Documents/Sports Interactive/Football Manager 2024/'
        else:
            self.data_dir = data_dir

    def _load_html_file(filepath: str):
        if filepath is None:
            filepath = get_latest_file(self.data_dir)

        return pd.read_html(self.data_dir+filepath, header=0, encoding='utf-8')[0]  

    def read_html(self, filepath=None):
        data = self._load_html_file(filepath)
        data = data.astype({col:str for col in columns})

        # init list of series objects to paste on to the end of the dataframe
        series_list = []
        for col_name, series in data.items():
            # Remove the .(digits) from the end of the column name
            col_name = re.split('\.\d', col_name, maxsplit=0)[0]

            # Nationality and Natural Fitness have the same name, handle that here
            if col_name == 'Nat':
                # Natural Fitness will never have a mean len above two
                if series.apply(lambda x: len(x)).mean() > 2:
                    series.name = 'Nation'
                    series_list.append(series.copy())
                    continue
            func = parse_mapping[col_name]



            if func is not None:
                series_list.append(series.apply(lambda x: func(x)).copy())
            else:
                series_list.append(series)

        return pd.concat(series_list, axis=1)
