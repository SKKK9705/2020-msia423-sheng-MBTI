import datetime
import sqlalchemy
import yaml
from sqlalchemy.orm import sessionmaker
import logging
import os
import sqlalchemy as sql

logging.basicConfig(level = logging.DEBUG, format = '%(name)-12s %(levelname)-8s %(message)s')
logger = logging.getLogger()


def get_connection():
    """
    function to return RDS database engine string
    :return: sqlalchemy database uri
    """
    conn_type = "mysql+pymysql"
    user = os.environ.get("MYSQL_USER")
    password = os.environ.get("MYSQL_PASSWORD")
    host = os.environ.get("MYSQL_HOST")
    port = os.environ.get("MYSQL_PORT")
    DATABASE_NAME = 'msia423_db'
    SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, DATABASE_NAME)
    return SQLALCHEMY_DATABASE_URI


def get_session(engine_string = None):
    """
    Args:
        engine_string: SQLAlchemy connection string in the form of:
            "{sqltype}://{username}:{password}@{host}:{port}/{database}"
    Returns:
        SQLAlchemy session
    """

    if engine_string is None:
        return ValueError("engine_string` must be provided")
    engine = sql.create_engine(engine_string)
    Session = sessionmaker(bind=engine)
    session = Session()

    return session
