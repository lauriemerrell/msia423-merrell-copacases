import logging
import pandas as pd
import pytest
from src import clean_copa_data as ccd

logger = logging.getLogger("test_clean_copa_data")

# reference: https://docs.pytest.org/en/latest/assert.html#assertions-about-expected-exceptions

def test_drop_too_recent_happy():
    """Test that dates after 5/10/2020 are dropped."""
    data = pd.read_csv("test/test_data.csv")
    orig_len = len(data)
    data_drop = ccd.drop_too_recent(data)
    new_len = len(data_drop)
    assert new_len == orig_len - 1

def test_drop_too_recent_unhappy():
    """When column is missing."""
    with pytest.raises(KeyError, match=r".*COMPLAINT_DATE.*"):
        ccd.drop_too_recent(pd.DataFrame())

def test_drop_status_asst_happy():
    """Valid input for drop_status_asst."""
    data = pd.read_csv("test/test_data.csv")
    orig_len = len(data)
    data_drop = ccd.drop_status_asst(data)
    new_len = len(data_drop)
    assert new_len == orig_len - 1

def test_drop_status_asst_unhappy():
    """When column is missing."""
    with pytest.raises(KeyError, match=r".*ASSIGNMENT.*"):
        ccd.drop_status_asst(pd.DataFrame())

def test_drop_nas_happy():
    """Valid input for drop_nas."""
    data = pd.read_csv("test/test_data.csv")
    orig_len = len(data)
    data_drop = ccd.drop_nas(data)
    new_len = len(data_drop)
    assert new_len == orig_len - 1

def test_drop_nas_unhappy():
    """When column is missing."""
    with pytest.raises(KeyError, match=r".*RACE_OF_COMPLAINANTS.*"):
        ccd.drop_nas(pd.DataFrame())

def test_drop_multiples_happy():
    """Valid input for drop_nas."""
    data = pd.read_csv("test/test_data.csv")
    orig_len = len(data)
    data_drop = ccd.drop_nas(data)
    new_len = len(data_drop)
    assert new_len == orig_len - 1

def test_drop_multiples_unhappy():
    """When column is missing."""
    with pytest.raises(KeyError, match=r".*RACE_OF_COMPLAINANTS.*"):
        ccd.drop_multiples(pd.DataFrame())

def test_drop_multiples_happy():
    """Valid input for drop_nas."""
    data = pd.read_csv("test/test_data.csv")
    orig_len = len(data)
    data_drop = ccd.drop_nas(data)
    new_len = len(data_drop)
    assert new_len == orig_len - 1

def test_drop_multiples_unhappy():
    """When column is missing."""
    with pytest.raises(KeyError, match=r".*RACE_OF_COMPLAINANTS.*"):
        ccd.drop_multiples(pd.DataFrame())

def test_make_excessive_force_happy():
    """Valid input for drop_nas."""
    data = pd.read_csv("test/test_data.csv")
    data_exf = ccd.make_excessive_force(data)
    assert data_exf['EXCESSIVE_FORCE'][1] == True

# approach taken from: https://stackoverflow.com/questions/53125305/testing-logging-output-with-pytest
def test_make_excessive_force_unhappy(caplog):
    """When column is missing."""
    with caplog.at_level(logging.ERROR):
        ccd.make_excessive_force(pd.DataFrame())
    assert "CURRENT_CATEGORY" in caplog.text
