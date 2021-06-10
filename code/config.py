
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_uri = f'postgresql:postgres:{os.environ['DBPASSWORD']}@fraudbnb-db.cysu6ff5rfrq.us-west-2.rds.amazonaws.com:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.urandom(24) # For WTF forms