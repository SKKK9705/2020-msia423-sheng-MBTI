import os
import sys
import argparse
import yaml

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
    words_per_comment = Column(sql.Float, unique=False, nullable=False)
    http_per_comment = Column(sql.Float, unique=False, nullable=False)
    music_per_comment = Column(sql.Float, unique=False, nullable=False)
    question_per_comment = Column(sql.Float, unique=False, nullable=False)
    img_per_comment = Column(sql.Float, unique=False, nullable=False)
    excl_per_comment = Column(sql.Float, unique=False, nullable=False)
    ellipsis_per_comment = Column(sql.Float, unique=False, nullable=True)
    I_E = Column(Integer, unique=False, nullable=True)
    N_S = Column(Integer, unique=False, nullable=True)
    T_F = Column(Integer, unique=False, nullable=True)
    J_P = Column(Integer, unique=False, nullable=True)
    type = Column(String(100), unique=False, nullable=True)

    def __repr__(self):
        users_repr = "<posts(id='%s', posts='%s', words_per_comment='%s', http_per_comment='%s', " \
                     "music_per_comment='%s', question_per_comment='%s', img_per_comment='%s', " \
                     "excl_per_comment='%s', ellipsis_per_comment='%s' , I_E='%s', N_S='%s', T_F='%s', J_P='%s',, type='%s')>"
        return users_repr % (self.id, self.posts, self.words_per_comment, self.http_per_comment, self.music_per_comment,
                             self.ellipsis_per_comment, self.question_per_comment, self.img_per_comment, self.excl_per_comment,self.ellipsis_per_comment, self.I_E, self.N_S, self.T_F, self.J_P, self.type)



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

    user = User(posts=args.posts, words_per_comment=args.words_per_comment, http_per_comment=args.http_per_comment, music_per_comment=args.music_per_comment, question_per_comment=args.question_per_comment, img_per_comment=args.img_per_comment, excl_per_comment=args.excl_per_comment, ecllipsis_per_comment=args.ellipsis_per_comment, I_E=args.I_E, N_S=args.N_S, T_F=args.T_F, J_P=args.J_P, type=args.type type=args.type)
    session.add(user)
    session.commit()
    logger.info(
        "Database created with user info added, Post: %s, Word per Comment: %s, http per Comment: %s, Music per Comment: %s, "
        "Question per Comment: %s, Image per Comment: %s, Exclamation per Comment: %s, Ellipsis per Comment: %s, I_E: %s, N_S: %s, T_F: %s, J_P: %s, Type: %s",
        args.posts, args.words_per_comment, args.http_per_comment, args.music_per_comment, args.question_per_comment, args.img_per_comment, args.excl_per_comment,
        args.ellipsis_per_comment, args.I_E, args.N_S, args.T_F, args.J_P, args.type)

    session.close()


def add_user(args):
    """Seeds an existing database with additional users whose personality will be predicted
    Args:
        args: Argparse args - should include args. all fields I listed above
    Returns:None
    """

    RDS = eval(args.RDS)
    if RDS is True:
        engine_string = get_connection()
    else:
        engine_string = args.enging_string

    engine = sql.create_engine(engine_string)

    Base.metadata.create_all(engine)
    logger.info('database created')

    session = get_session(engine_string=engine_string)
