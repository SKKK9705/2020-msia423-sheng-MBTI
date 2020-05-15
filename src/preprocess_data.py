import pandas as pd
import yaml
import argparse
import logging
import statistics
from src.load_data import load_csv

logging.basicConfig(level = logging.DEBUG, format = '%(name)-12s %(levelname)-8s %(message)s')
logger = logging.getLogger()


def generate_class(df, target=None, response1=None, response2=None, response3=None, response4=None, **kwargs):
    """
    split one response into four categories and binarize them
    :param df: raw dataframe
    :param target: column used to generate binary response
    :param response1: column I-E
    :param response2: column N-S
    :param response3: column T-F
    :param response4: column J-P
    :return: dataframe with four new columns
    """

    map1 = {"I": 0, "E": 1}
    map2 = {"N": 0, "S": 1}
    map3 = {"T": 0, "F": 1}
    map4 = {"J": 0, "P": 1}
    df[response1] = df[target].astype(str).str[0]
    df[response1] = df[response1].map(map1)
    df[response2] = df[target].astype(str).str[1]
    df[response2] = df[response2].map(map2)
    df[response3] = df[target].astype(str).str[2]
    df[response3] = df[response3].map(map3)
    df[response4] = df[target].astype(str).str[3]
    df[response4] = df[response4].map(map4)

    logger.info("binary class added to dataframe with column %s", response1, response2, response3, response4)
    return df


def run_class(args):
    with open(args.config, 'r') as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)

    df = load_csv(**config['load_data']['load_csv'])
    df = generate_class(df, **config['preprocess_data']['generate_class'])
    logger.info('data preprocess completed')

    df.to_csv(args.output, index=False)
    logger.info('data saved to %s', args.output)
    return df
