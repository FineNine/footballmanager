import pytest
import pandas as pd

from footballmanager.analysis.index import FMIndex

@pytest.fixture
def pandas_df():
    return pd.DataFrame([
        {'name':'derrick','acc':1,'pac':2,'wor':3},
        {'name':'domo','acc':4,'pac':5,'wor':6},
        {'name':'chad','acc':0,'pac':6,'wor':0},
        {'name':'chad2','acc':1,'pac':1,'wor':1},
        {'name':'bichael','acc':None,'pac':0,'wor':None},
    ])

def test_df(pandas_df):
    print("\n", pandas_df)
    assert len(pandas_df) == 5

@pytest.fixture
def test_index():
    return FMIndex(
        name = "test_index",
        weighting_dict = {
                'A':{
                    'acc':1
                },
                'acc':97, 
                'pac':100,
                'wor':0,
                'B':{
                    'acc':2,
                    'pac':0
                }
            }
    )

def test_compute_layers(pandas_df, test_index):
    data = test_index.compute(pandas_df, sort=False)
    assert data['test_index'].iloc[0] == 1.5
    assert data['test_index'].iloc[1] == 4.5
    assert data['test_index'].iloc[2] == 3.0
    assert data['test_index'].iloc[3] == 1.0

    print(data)
