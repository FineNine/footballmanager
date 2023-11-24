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

    def read_html(self, filepath=None):
        if filepath is None:
            filepath = get_latest_file(self.data_dir)
        
        data = pd.read_html(self.data_dir+filepath, header=0, encoding='utf-8')[0]
        columns = [re.split('\.\d', col, maxsplit=0)[0] for col in data.columns]
        data = data.astype({col:str for col in columns})

        for col in columns:
            func = parse_mapping[col]
            if func is not None:
                data[col] = data[col].apply(lambda x: func(x))

        return data
