import glob
import os

def get_latest_file(directory: str) -> str:
    list_of_files = glob.glob(os.path.join(directory, '*'))
    return max(list_of_files, key=os.path.getctime)

