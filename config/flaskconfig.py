import os
DEBUG = True
LOGGING_CONFIG = "config/logging/local.conf"
PORT = 5000
APP_NAME = "mbti-prediction"
SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = "0.0.0.0"
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100


DB_USER = os.environ.get("MYSQL_USER")
DB_PW = os.environ.get("MYSQL_PASSWORD")
DB_HOST = os.environ.get("MYSQL_HOST")
DB_PORT = os.environ.get("MYSQL_PORT")
DATABASE = os.environ.get("DATABASE_NAME")
DB_DIALECT = "mysql+pymysql"
SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")

if SQLALCHEMY_DATABASE_URI is not None:
    pass
elif DB_HOST is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data/users.db'
else:
    SQLALCHEMY_DATABASE_URI = '{dialect}://{user}:{pw}@{host}:{port}/{db}'.format(dialect=DB_DIALECT, user=DB_USER,
                                                                                  pw=DB_PW, host=DB_HOST, port=DB_PORT,
                                                                                  db=DATABASE)
