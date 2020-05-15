import argparse

from src.load_data import run_load
from src.preprocess_data import run_class
from src.generate_feature import run_features
from src.add_users import create_db, add_user

if __name__ == '__main__':

    # Add parsers for both creating a database and adding songs to it
    parser = argparse.ArgumentParser(description="Create and/or add data to database")
    subparsers = parser.add_subparsers()

    # Sub-parser for creating a database
    sb_create = subparsers.add_parser("create_db", description="Create database")
    sb_create.add_argument("--posts", default="I am a post!", help="User post input to be added")
    sb_create.add_argument("--words_per_comment", default=20.0, help="word per comment of user posts to be added")
    sb_create.add_argument("--http_per_comment", default=1.0, help="number of http included per comment being added.")
    sb_create.add_argument("--music_per_comment", default=1.0, help="number of music per comment being added.")
    sb_create.add_argument("--question_per_comment", default=1.0, help="number of questions per comment being added.")
    sb_create.add_argument("--img_per_comment", default=1.0, help="number of image per comment being added.")
    sb_create.add_argument("--excl_per_comment", default=5.0, help="number of exclamation marks per comment being added.")
    sb_create.add_argument("--ellipsis_per_comment", default=2.0, help="number of ellipsis per comment being added.")
    sb_create.add_argument("--I_E", default=None, help="introversion vs extraversion prediction being added.")
    sb_create.add_argument("--N_S", default=None, help="intuition vs sensing prediction being added.")
    sb_create.add_argument("--T_F", default=None, help="thinking vs feeling prediction being added.")
    sb_create.add_argument("--J_P", default=None, help="perception vs judgment prediction being added.")
    sb_create.add_argument("--type", default=None, help="overall mbti type being added.")
    sb_create.add_argument("--engine_string", default='sqlite:///data/users.db', help="SQLAlchemy connection URI for database")
    sb_create.add_argument('--RDS', default='True', help='True to use RDS')
    sb_create.set_defaults(func=create_db)

    # Sub-parser for ingesting new data
    sb_ingest = subparsers.add_parser("ingest", description="Add data to database")
    sb_ingest.add_argument("--artist", default="Emancipator", help="Artist of song to be added")
    sb_ingest.add_argument("--title", default="Minor Cause", help="Title of song to be added")
    sb_ingest.add_argument("--album", default="Dusk to Dawn", help="Album of song being added")
    sb_ingest.add_argument("--engine_string", default='sqlite:///data/tracks.db',
                           help="SQLAlchemy connection URI for database")
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

    args = parser.parse_args()
    args.func(args)
