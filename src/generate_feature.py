import pandas as pd
import yaml
import argparse
import logging
from src.load_data import load_csv

logging.basicConfig(level=logging.DEBUG, format='%(name)-12s %(levelname)-8s %(message)s')
logger = logging.getLogger()


def add_feature(path=None, target=None, f1=None, f2=None, f3=None, f4=None, f5=None, f6=None, f7=None, **kwargs):
    """
    add seven new features to the dataframe
    :param path: input path of data
    :param target: column name of the posts
    :param f1: words per comment
    :param f2: http per comment
    :param f3: music per comment
    :param f4: question per comment
    :param f5: image per comment
    :param f6: exclamation per comment
    :param f7: ellipsis per comment
    :return: a dataframe with features added
    """
    # read in raw data
    df = pd.read_csv(path)

    # generate new features based by taking the average of the occurances of punctuations and others
    df[f1] = df[target].apply(lambda x: len(x.split()) / 50)
    df[f2] = df[target].apply(lambda x: x.count('http') / 50)
    df[f3] = df[target].apply(lambda x: x.count('music') / 50)
    df[f4] = df[target].apply(lambda x: x.count('?') / 50)
    df[f5] = df[target].apply(lambda x: x.count('jpg') / 50)
    df[f6] = df[target].apply(lambda x: x.count('!') / 50)
    df[f7] = df[target].apply(lambda x: x.count('...') / 50)
    logger.info('seven new features are generated')
    return df


def run_features(args):
    with open(args.config, 'r') as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)

    df = add_feature(**config['generate_feature']['add_feature'])
    logger.info('dataframe for model created')
    df.to_csv(args.output, index=False)
    logger.info('data for model saved to %s', args.output)
    return df
