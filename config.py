# coding=utf-8
import os


class Configuration:
    DEBUG = True
    current_path = os.path.dirname(os.path.abspath(__file__))

    # flask_sqlalchemy config
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(current_path, 'data.sqlite'))
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
