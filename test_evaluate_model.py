from src.evaluate_model import evaluate_model
from src.evaluate_model import post_process
import pandas as pd
import yaml
import numpy as np
from pandas.testing import assert_frame_equal
import pickle
import sklearn
from sklearn import metrics
import pytest

with open('config/config.yml', 'r') as f:
    config = yaml.load(f)

def test_evaluate_model_happy():
    """test the functionality of evaluating model with happy path"""

    # read in and open model, x_test and y_test files
    modelpath = 'models/modelie.pkl'
    xtestpath = 'test/test_evaluate_model_x_test_happy.csv'
    yietestpath = 'test/test_evaluate_model_y_test_happy.csv'

    with open(modelpath, "rb") as f:
        expected_lr = pickle.load(f)

    X_test = pd.read_csv(xtestpath, header = 0)
    y_test = pd.read_csv(yietestpath, header = None)
    # get probability and corresponding bins of predictions
    ypred_proba_test = expected_lr.predict_proba(X_test)[:, 1]
    ypred_bin_test = expected_lr.predict(X_test)

    # calculate expected auc and accuracy for good inputs
    expected_auc = sklearn.metrics.roc_auc_score(y_test, ypred_proba_test)
    expected_accuracy = sklearn.metrics.accuracy_score(y_test, ypred_bin_test)

    # true auc and accuracy
    true_auc, true_confusion, true_accuracy = evaluate_model(yietestpath, modelpath, xtestpath)

    # check to see if two of them equal
    assert true_auc == expected_auc
    assert true_accuracy == expected_accuracy


def test_evaluate_model_unhappy():
    """test the functionality of evaluating model with unhappy path"""
    # read in and open model, x_test and y_test files
    modelpath = 'models/modelie.pkl'
    xtestpath = 'test/test_evaluate_model_x_test_unhappy.csv'
    yietestpath = 'test/test_evaluate_model_y_test_unhappy.csv'

    with open(modelpath, "rb") as f:
        expected_lr = pickle.load(f)

    X_test = pd.read_csv(xtestpath, header = 0)
    y_test = pd.read_csv(yietestpath, header = None)

    # get probability and corresponding bins of predictions
    ypred_proba_test = expected_lr.predict_proba(X_test)[:, 1]
    ypred_bin_test = expected_lr.predict(X_test)

    # calculate expected auc and accuracy for good inputs
    expected_auc = sklearn.metrics.roc_auc_score(y_test, ypred_proba_test)
    expected_accuracy = sklearn.metrics.accuracy_score(y_test, ypred_bin_test)

    # true auc and accuracy
    true_auc, true_confusion, true_accuracy = evaluate_model(yietestpath, modelpath, xtestpath)

    # check to see if two of them equal
    assert true_auc == expected_auc
    assert true_accuracy == expected_accuracy


def test_post_process_happy():
    """test the functionality of post processing with happy path"""
    # read in and open model files
    modelpath = 'models/modelie.pkl'
    features = config['evaluate_model']['post_process']['features']

    with open(modelpath, "rb") as f:
        lr = pickle.load(f)
    # get the expected fitted feature importance and odd ratios
    fitted = pd.DataFrame(index=features)
    fitted['coefs'] = lr.coef_[0]
    fitted['odds_ratio'] = fitted.coefs.apply(np.exp)
    expected_fitted = fitted.sort_values(by='odds_ratio', ascending=False)
    # true feature importance and odds ratios
    true_fitted = post_process(modelpath, **config['evaluate_model']['post_process'])
    # check if two of them equal
    assert expected_fitted.equals(true_fitted)


def test_post_process_unhappy():
    """test the functionality of post processing with unhappy path"""
    # read in and open model files
    modelpath = 'models/modeljp.pkl'
    features = config['evaluate_model']['post_process']['features']

    with open(modelpath, "rb") as f:
        lr = pickle.load(f)
    # get the expected fitted feature importance and odd ratios
    fitted = pd.DataFrame(index=features)
    fitted['coefs'] = lr.coef_[0]
    fitted['odds_ratio'] = fitted.coefs.apply(np.exp)
    expected_fitted = fitted.sort_values(by='odds_ratio', ascending=False)
    # true feature importance and odds ratios
    true_fitted = post_process(modelpath, **config['evaluate_model']['post_process'])
    # check if two of them equal
    assert expected_fitted.equals(true_fitted)




