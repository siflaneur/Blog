# coding=utf-8
from app import app


@app.route('/')
def homepage():
    return 'Hello world!'

