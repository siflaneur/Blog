# coding=utf-8
import os, sys
sys.path.append(os.getcwd())

from manage import db

if __name__ == '__main__':
    db.create_all()
