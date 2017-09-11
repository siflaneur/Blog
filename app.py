# coding=utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_wtf.csrf import CsrfProtect
from flask_bootstrap import Bootstrap

from config import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migration = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
