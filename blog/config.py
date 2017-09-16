# coding=utf-8
import os


class Configuration:
    DEBUG = True
    SECRET_KEY = 'XXXXXXXXX'
    current_path = os.path.dirname(os.path.abspath(__file__))

    # file that stores the image
    STATIC_DIR = os.path.join(current_path, 'static')
    IMAGES_DIR = os.path.join(STATIC_DIR, 'images')

    # flask_sqlalchemy config
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(current_path, 'data.sqlite'))
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
