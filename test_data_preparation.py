from src.preprocess_data import generate_class
from src.generate_feature import add_feature
import pandas as pd
import yaml
import numpy as np
from pandas.testing import assert_frame_equal
import pytest

with open('config/config.yml', 'r') as f:
    config = yaml.load(f)


def test_generate_class_happy():
    """ test the functionality of generating class with happy path"""
    # read in happy input
    input = {'target': ['INFP','ISTP']}
    input_df = pd.DataFrame(data=input)
    # expected results
    expected = {'target': ['INFP','ISTP'],
                'I-E': [0,0],
                'N-S': [0,1],
                'T-F': [1,0],
                'J-P': [1,1]
                }
    expected_df = pd.DataFrame(data=expected)
    # true results
    true_df = generate_class(input_df,'target','I-E','N-S','T-F','J-P')

    # Check if twp of them equal
    assert_frame_equal(expected_df, true_df)


def test_generate_class_unhappy():
    """ test the functionality of generating class with unhappy path"""
    # read in unhappy input
    input = {'target': ['ABCD', 'FGHK']}
    input_df = pd.DataFrame(data=input)
    # expected results
    expected = {'target': ['ABCD', 'FGHK'],
                'I-E': [np.nan, np.nan],
                'N-S': [np.nan, np.nan],
                'T-F': [np.nan, np.nan],
                'J-P': [np.nan, np.nan]
                }
    expected_df = pd.DataFrame(data=expected)
    # true results
    true_df = generate_class(input_df, 'target', 'I-E', 'N-S', 'T-F', 'J-P')

    # Check if twp of them equal
    assert_frame_equal(expected_df, true_df)


def test_generate_feature_happy():
    """ test the functionality of generating features with happy path"""
    # expected results
    expected = {'posts': ['http music ? jpg !'],
                'words_per_comment': [5/50],
                'http_per_comment': [1/50],
                'music_per_comment': [1/50],
                'question_per_comment': [1/50],
                'img_per_comment': [1/50],
                'excl_per_comment': [1/50],
                'ellipsis_per_comment': [0.0]
                }
    expected_df = pd.DataFrame(data=expected)

    # read in happy input
    test_path = 'test/test_generate_feature_happy.csv'
    # true results
    true_df = add_feature(test_path, 'posts', 'words_per_comment', 'http_per_comment', 'music_per_comment',
                             'question_per_comment', 'img_per_comment', 'excl_per_comment', 'ellipsis_per_comment')

    # Check if twp of them equal
    assert_frame_equal(expected_df, true_df)


def test_generate_feature_unhappy():
    """ test the functionality of generating features with unhappy path"""
    # expected results
    expected = {'posts': ['jjjjjj'],
                'words_per_comment': [1/50],
                'http_per_comment': [0.0],
                'music_per_comment': [0.0],
                'question_per_comment': [0.0],
                'img_per_comment': [0.0],
                'excl_per_comment': [0.0],
                'ellipsis_per_comment': [0.0]
                }
    expected_df = pd.DataFrame(data=expected)

    # read in happy input
    test_path = 'test/test_generate_feature_unhappy.csv'
    # true results
    true_df = add_feature(test_path, 'posts', 'words_per_comment', 'http_per_comment', 'music_per_comment',
                             'question_per_comment', 'img_per_comment', 'excl_per_comment', 'ellipsis_per_comment')

    # Check if twp of them equal
    assert_frame_equal(expected_df, true_df)

