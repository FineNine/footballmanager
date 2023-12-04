import pytest
from pathlib import WindowsPath, Path
from pandas import DataFrame

from footballmanager.io import (
    _OS_USERNAME,
    find_latest_file,
    load_export,
    parse_percent
)

# @pytest.fixture
# def 


# Tests
@pytest.mark.parametrize(
        'test_input,expected',[("0%", 0),("19%",.19),("100%", 1)]
)
def test_parse_percent(test_input, expected):
    assert parse_percent(test_input) == expected

def test_username():
    assert type(_OS_USERNAME) == str

def test_find_latest_file(tmp_path):
    # tmp_path.mkdir()
    temp_file1: WindowsPath = tmp_path / "test1.txt"
    temp_file2: WindowsPath = tmp_path / "test1.txt"
    temp_file1.write_text("TESTING")
    temp_file2.write_text("TESTING")
    

    latest_file = find_latest_file(tmp_path)
    assert len(list(tmp_path.iterdir())) == 1
    assert  type(latest_file) == str
    assert  WindowsPath(latest_file) == temp_file2

def test_load_export():
    data = load_export("tests/test_player_search.html")
    
    assert type(data) == DataFrame
    assert len(data) == 47

    # [print(col, data[col].dtype) for col in data.columns]

    data.to_csv('tests/test_player_search.csv', index=False)