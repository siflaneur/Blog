# coding=utf-8
from app import manager, app, db
import views
import models

from entries.blueprint import entries
app.register_blueprint(entries, url_prefix='/entries')


if __name__ == '__main__':
    manager.run()
