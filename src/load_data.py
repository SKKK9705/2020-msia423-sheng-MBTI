import pandas as pd
import yaml
import argparse
import logging
import boto3

logging.basicConfig(level=logging.DEBUG, format='%(name)-12s %(levelname)-8s %(message)s')
logger = logging.getLogger()


def download_data(path=None, **kwargs):
    """
    download data
    :param path: pth to raw data
    :return: none
    """

    url = 'https://media.githubusercontent.com/media/SKKK9705/msia423/master/mbti.csv'
    df = pd.read_csv(url, index_col=0)
    df.to_csv(path)
    logger.info("data saved to %s", path)


def upload_data(input_path=None, bucket_name=None, output_path=None, **kwargs):
    """
    upload data to s3 bucket
    :param input_path: path where data is saved locally
    :param bucket_name: name of the s3 bucket
    :param output_path: s3 bucket path
    :return: none
    """

    s3 = boto3.client('s3')
    s3.upload_file(input_path, bucket_name, output_path)
    logger.info("data uploaded to s3 bucket")


def load_csv(path=None, **kwargs):
    """
    read data to pd for modeling purposes
    :param path: local path to data
    :return: pd
    """

    df = pd.read_csv(path, header=0)
    logger.info("data read from %s", path)
    return df


def run_load(args):
    with open(args.config, 'r') as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)

    download_data(**config['load_data']['download_data'])
    upload_data(**config['load_data']['upload_data'])
    df = load_csv(**config['load_data']['load_csv'])
    logger.info("data loaded as dataframe")
    return df
