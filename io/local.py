import pandas
import glob
import os
from .tools import get_latest_file

class FMLoader():
    def __init__(self, data_dir: str = None):
        self.data_dir = data_dir

    def read_html(self, filepath=None):
        if filepath is None:
            filepath = get_latest_file(self.data_dir)
            print(filepath)
