import pytest
import pandas as pd

from footballmanager.analysis.index import FMIndex

@pytest.fixture
def pandas_df():
    return pd.DataFrame([
        {'name':'derrick','acc':1,'pac':2,'wor':3},
        {'name':'domo','acc':4,'pac':5,'wor':6},
        {'name':'chad','acc':0,'pac':0,'wor':0},
        {'name':'bichael','acc':None,'pac':0,'wor':None},
    ])

def test_df(pandas_df):
    print("\n", pandas_df)
    assert len(pandas_df) == 4

@pytest.fixture
def test_index():
    return FMIndex