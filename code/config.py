import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = \
        'postgresql://postgres:msds603-8@fraudbnb-8-1.cysu6ff5rfrq.us-west-2.rds.amazonaws.com:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
