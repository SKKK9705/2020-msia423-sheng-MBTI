from src.train_model import split_data
from src.train_model import train
import pandas as pd
import yaml
import numpy as np
from pandas.testing import assert_frame_equal
import sklearn
from sklearn import linear_model
import pickle
import pytest

with open('config/config.yml', 'r') as f:
    config = yaml.load(f)


def test_split_data_happy():
    """ test the functionality of splitting data with happy path"""
    # test data
    test_path = config['evaluate_model']['evaluate_model']['xtestpath']
    df_test = pd.read_csv(test_path, header=0)
    # original data
    file_path = config['train_model']['split_data']['path']
    df_origin = pd.read_csv(file_path, header=0)
    # number of rows of test and original whole dataset
    test_row = df_test.shape[0]
    origin_row = df_origin.shape[0]
    # calculate the expected percentage
    expected_percentage = test_row / origin_row
    # true percentage
    true_percent = config['train_model']['split_data']['test_size']
    # tolerant error range
    low = true_percent - 0.02
    high = true_percent + 0.02
    # if the expected value fall within the tolerant error range
    assert expected_percentage > low
    assert expected_percentage < high


def test_split_data_unhappy():
    """ test the functionality of splitting data with unhappy path"""
    # read in bad input with no rows of data
    input = {'words_per_comment': [],
             'http_per_comment': [],
             'music_per_comment': [],
             'question_per_comment': [],
             'img_per_comment': [],
             'excl_per_comment': [],
             'ellipsis_per_comment': []
            }
    input_df = pd.DataFrame(data=input)

    file_path = config['train_model']['split_data']['path']
    origin_df = pd.read_csv(file_path, header=0)

    input_row = input_df.shape[0]
    origin_row = origin_df.shape[0]

    expected_percentage = input_row / origin_row
    # check if expected results from bad input equal to 0
    assert expected_percentage == 0


def test_train_happy():
    """ test the functionality of training the model with happy path"""
    # read and open model file
    modeliepath = 'models/modelie.pkl'
    with open(modeliepath, "rb") as f:
        modelie = pickle.load(f)

    # convert to a dataframe of good feature inputs
    X = pd.DataFrame({'words_per_comment': [5],
                      'http_per_comment': [0],
                      'music_per_comment': [0],
                      'question_per_comment': [3],
                      'img_per_comment': [0],
                      'excl_per_comment': [6],
                      'ellipsis_per_comment': [0]})
    # expected prediction from the model with good inputs
    expected_ie = modelie.predict(X)
    # check if expected prediction equals true prediction
    assert expected_ie == 1


def test_train_unhappy():
    """ test the functionality of training the model with unhappy path"""
    # read and open model file
    modeliepath = 'models/modelie.pkl'
    with open(modeliepath, "rb") as f:
        modelie = pickle.load(f)

    # convert to a dataframe of bad feature inputs
    X = pd.DataFrame({'words_per_comment': [0],
                      'http_per_comment': [0],
                      'music_per_comment': [0],
                      'question_per_comment': [0],
                      'img_per_comment': [0],
                      'excl_per_comment': [0],
                      'ellipsis_per_comment': [0]})
    # expected prediction from the model with bad input
    expected_ie = modelie.predict(X)
    # check if expected prediction equals true prediction
    assert expected_ie == 0






