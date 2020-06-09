import os
import sys
import argparse
import yaml
import pickle
import pandas as pd

from sqlalchemy import create_engine, Column, Integer, String, Text, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sql
from src.helpers import get_session, get_connection

import logging

logger = logging.getLogger(__name__)
logger.setLevel("INFO")

Base = declarative_base()

class User(Base):
    """
    Create a data model for the database to be set up for capturing posts
    """
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True)
    posts = Column(Text, unique=False, nullable=False)
    type = Column(String(100), unique=False, nullable=True)

    def __repr__(self):
        users_repr = "<posts(id='%s', posts='%s', type='%s')>"
        return users_repr % (self.id, self.posts, self.type)


def create_db(args):
    """
    Creates a database with the data model given by obj:`apps.models.Posts`
    Args:
        args: Argparse args - should include args.all fields listed above
    Returns: None
    """

    RDS = eval(args.RDS)
    if RDS is True:
        engine_string = get_connection()
    else:
        engine_string = args.engine_string

    engine = sql.create_engine(engine_string)

    Base.metadata.create_all(engine)
    logger.info('database created')

    session = get_session(engine_string=engine_string)

<<<<<<< HEAD
    user = User(posts=args.posts)
||||||| merged common ancestors
    user = User(posts=args.posts, words_per_comment=args.words_per_comment, http_per_comment=args.http_per_comment, music_per_comment=args.music_per_comment, question_per_comment=args.question_per_comment, img_per_comment=args.img_per_comment, excl_per_comment=args.excl_per_comment, ecllipsis_per_comment=args.ellipsis_per_comment, I_E=args.I_E, N_S=args.N_S, T_F=args.T_F, J_P=args.J_P, type=args.type)
=======
    user = User(posts=args.posts, words_per_comment=args.words_per_comment, http_per_comment=args.http_per_comment, music_per_comment=args.music_per_comment, question_per_comment=args.question_per_comment, img_per_comment=args.img_per_comment, excl_per_comment=args.excl_per_comment, ellipsis_per_comment=args.ellipsis_per_comment, I_E=args.I_E, N_S=args.N_S, T_F=args.T_F, J_P=args.J_P, type=args.type)
>>>>>>> a77afaf4e5d48a96770652ef76529895285f4280
    session.add(user)
    session.commit()
    logger.info(
        "Database created with user info added, Post: %s", args.posts)

    session.close()


def add_user(args):
    """Seeds an existing database with additional users whose personality will be predicted
    Args:
        args: Argparse args - should include args. all fields I listed above
    Returns:None
    """

    # get engine string set up either local database or RDS instance
    RDS = eval(args.RDS)
    if RDS is True:
        engine_string = get_connection()
    else:
        engine_string = args.engine_string

    # start a session
    session = get_session(engine_string=engine_string)

    # read user input
    posts = str(args.posts)

    # create features from raw user input
    words_per_comment = len(posts.split())
    http_per_comment = posts.count('http')
    music_per_comment = posts.count('music')
    question_per_comment = posts.count('?')
    img_per_comment = posts.count('jpg')
    excl_per_comment = posts.count('!')
    ellipsis_per_comment = posts.count('...')

    # create a dataframe to store all features extracted from user input
    X = pd.DataFrame({'words_per_comment': [words_per_comment], 'http_per_comment': [http_per_comment], 'music_per_comment': [music_per_comment],
                      'question_per_comment': [question_per_comment], 'img_per_comment': [img_per_comment],
                      'excl_per_comment': [excl_per_comment], 'ellipsis_per_comment': [ellipsis_per_comment]})

    # use pretrained models to make predictions
    with open('models/modelie.pkl', "rb") as f:
        modelie = pickle.load(f)
    Class_ie = modelie.predict(X)
    if Class_ie == 0:
        Output_ie = 'I'
    else:
        Output_ie = 'E'

    with open('models/modeljp.pkl', "rb") as f:
        modeljp = pickle.load(f)
    Class_jp= modeljp.predict(X)
    if Class_jp == 0:
        Output_jp = 'J'
    else:
        Output_jp = 'P'

    with open('models/modelns.pkl', "rb") as f:
        modelns = pickle.load(f)
    Class_ns= modelns.predict(X)
    if Class_ns == 0:
        Output_ns = 'N'
    else:
        Output_ns = 'S'

    with open('models/modeltf.pkl', "rb") as f:
        modeltf = pickle.load(f)
    Class_tf= modeltf.predict(X)
    if Class_tf == 0:
        Output_tf = 'T'
    else:
        Output_tf = 'F'

    # concat final result
    type_output = Output_ie + (Output_ns) + (Output_tf) + (Output_jp)

    # add new user posts and corresponding prediction
    user = User(posts=args.posts, type=type_output)
    session.add(user)
    session.commit()
    logger.info(
        "new user added with personality type prediction: %s", type_output)
    session.close()
