import logging
import pandas as pd
import pytest
import sklearn
from src import train_copa_model as tcm

def test_train_test_split_happy():
    X_train, X_test, y_train, y_test = tcm.train_test_split("test/test_data.csv", ['ASSIGNMENT', 'CURRENT_CATEGORY'], 'FINDING_CODE', 4, .5)
    assert X_train.shape[1] == 2

def test_train_test_split_unhappy(caplog):
    with caplog.at_level(logging.ERROR):
        tcm.train_test_split("test/test_data.csv", ['ffff'], 'FINDING_CODE', 4, .5)
    assert "None" in caplog.text

def test_encode_data_happy():
    data = pd.read_csv("test/test_data.csv")
    data = data.dropna()
    denc, denc2, xenc = tcm.encode_data(data[['SEX_OF_COMPLAINANTS', 'CASE_TYPE']], data[['ASSIGNMENT', 'CASE_TYPE']])
    assert denc.shape[1] == 3

def test_encode_data_unhappy(caplog):
    data = pd.read_csv("test/test_data.csv")
    with caplog.at_level(logging.ERROR):
        tcm.encode_data(data, data)
    assert "NaN" in caplog.text

def test_fit_model_happy():
    data = pd.read_csv("test/test_data.csv")
    data = data.dropna()
    denc, denc2, xenc = tcm.encode_data(data[['SEX_OF_COMPLAINANTS', 'CASE_TYPE']], data[['ASSIGNMENT', 'CASE_TYPE']])
    model = tcm.fit_model(denc, data['FINDING_CODE'], 14)
    assert "GradientBoostingClassifier" in str(type(model))

def test_fit_model_unhappy(caplog):
    data = pd.read_csv("test/test_data.csv")
    data = data.dropna()
    denc, denc2, xenc = tcm.encode_data(data[['SEX_OF_COMPLAINANTS', 'CASE_TYPE']], data[['ASSIGNMENT', 'CASE_TYPE']])

    with caplog.at_level(logging.ERROR):
        tcm.fit_model(denc, denc2, 14)
    assert "shape" in caplog.text