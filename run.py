import argparse

from src.load_data import run_load
from src.preprocess_data import run_class
from src.generate_feature import run_features
from src.add_users import create_db, add_user
from src.train_model import run_train
from src.evaluate_model import run_evaluate

if __name__ == '__main__':

    # Add parsers for both creating a database and adding songs to it
    parser = argparse.ArgumentParser(description="Create and/or add data to database")
    #parser = argparse.ArgumentParser(add_help=False)
    subparsers = parser.add_subparsers()

    # Sub-parser for creating a database
    sb_create = subparsers.add_parser("create_db", description="Create database")
    sb_create.add_argument("--posts", default="I am a post!", help="User post input to be added")
    sb_create.add_argument("--type", default=None, help=" mbti type being added.")
    sb_create.add_argument("--engine_string", default='sqlite:///data/users.db', help="SQLAlchemy connection URI for database")
    sb_create.add_argument('--RDS', default='True', help='True to use RDS')
    sb_create.set_defaults(func=create_db)

    # Sub-parser for ingesting new user input
    sb_ingest = subparsers.add_parser("ingest", description="Add data to database")
    sb_ingest.add_argument("--posts", default="new post!", help="User post input to be added")
    sb_ingest.add_argument("--engine_string", default='sqlite:///data/users.db', help="SQLAlchemy connection URI for database")
    sb_ingest.add_argument('--RDS', default='True', help='True to use RDS')
    sb_ingest.set_defaults(func=add_user)

    # Sub-parser for ingesting loading the dataset
    sb_load = subparsers.add_parser('load_data', description='load data into dataframe')
    sb_load.add_argument('--config', default='config/config.yml', help='path to yaml file with configurations')
    sb_load.set_defaults(func=run_load)

    # Sub-parser for data pre-processing
    sb_preprocess = subparsers.add_parser('preprocess_data', description='add four binary classes to data')
    sb_preprocess.add_argument('--config', default='config/config.yml', help='path to yaml file with configurations')
    sb_preprocess.add_argument('--output', default='data/class_data.csv', help='path to save dataset')
    sb_preprocess.set_defaults(func=run_class)

    # Sub-parser for generating features
    sb_feature = subparsers.add_parser('generate_feature', description='generate features from posts content')
    sb_feature.add_argument('--config', default='config/config.yml', help='path to yaml file with configurations')
    sb_feature.add_argument('--output', default='data/model_data.csv', help='path to save dataset')
    sb_feature.set_defaults(func=run_features)

    # Sub-parser for training models
    sb_train = subparsers.add_parser('train_model', description='train a logistic regression model')
    sb_train.add_argument('--config', default='config/config.yml', help='path to yaml file with configurations')
    sb_train.add_argument('--xtestpath', default='data/xtest.csv', help='path to save x test')
    sb_train.add_argument('--ytestpathie', default='data/ytestie.csv', help='path to save y test')
    sb_train.add_argument('--ytestpathns', default='data/ytestns.csv', help='path to save y test')
    sb_train.add_argument('--ytestpathtf', default='data/ytesttf.csv', help='path to save y test')
    sb_train.add_argument('--ytestpathjp', default='data/ytestjp.csv', help='path to save y test')
    sb_train.add_argument('--modelpathie', default='models/modelie.pkl', help='path to save model')
    sb_train.add_argument('--modelpathns', default='models/modelns.pkl', help='path to save model')
    sb_train.add_argument('--modelpathtf', default='models/modeltf.pkl', help='path to save model')
    sb_train.add_argument('--modelpathjp', default='models/modeljp.pkl', help='path to save model')
    sb_train.set_defaults(func=run_train)

    # Sub-parser for evaluating models
    sb_evaluate = subparsers.add_parser('evaluate_model', description='evaluate models with metrics')
    sb_evaluate .add_argument('--config', default='config/config.yml', help='path to yaml file with configurations')
    sb_evaluate .add_argument('--output', default = 'models/evaluation.txt', help = 'path to save model evaluation')
    sb_evaluate.add_argument('--outputpost', default='models/post_process/', help='path to save feature importances/odd ratios')
    sb_evaluate .set_defaults(func=run_evaluate)

    args = parser.parse_args()
    args.func(args)
