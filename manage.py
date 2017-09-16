# coding=utf-8
from blog.app import manager, app, db
import blog.admin
import blog.views
import blog.models

from blog.entries.blueprint import entries
app.register_blueprint(entries, url_prefix='/entries')


if __name__ == '__main__':
    manager.run()
