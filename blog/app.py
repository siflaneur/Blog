# coding=utf-8
from flask import Flask, g, request, session
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_bootstrap import Bootstrap

from blog.config import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)

bcrypt = Bcrypt(app)
bootstrap = Bootstrap(app)


db = SQLAlchemy(app)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
migration = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = "login"


@app.before_request
def _before_request():
    g.user = current_user


@app.before_request
def _last_page_visted():
    if "current" in session:
        session["last_page"] = session["current_page"]
    session["current_page"] = request.path
