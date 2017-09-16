# coding=utf-8
import re
from datetime import datetime

from flask_login import UserMixin

from blog.app import db, login_manager, bcrypt


def slugify(s):
    return re.sub(r'[^\w]+', '-', s).lower()


entry_tags = db.Table('entry_tags',
                      db.Column('tags_id', db.Integer, db.ForeignKey('tags.id')),
                      db.Column('entries_id', db.Integer, db.ForeignKey('entries.id'))
                      )


class Entry(db.Model):
    __tablename__ = 'entries'
    STATUS_PUBLIC = 0
    STATUS_DRAFT = 1
    STATUS_DELETED = 2

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80))
    slug = db.Column(db.String(100), unique=True)
    body = db.Column(db.Text)
    created_timestamp = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.SmallInteger, default=STATUS_PUBLIC)
    modified_timestamp = db.Column(db.DateTime,
                                   default=datetime.now,
                                   onupdate=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    tags = db.relationship('Tag', secondary=entry_tags,
                           backref=db.backref('entries', lazy='dynamic'))
    comments = db.relationship('Comment', backref='entry', lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        self.slug = ''
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return '<Entry: {}>'.format(self.title)

    @property
    def tag_list(self):
        return ', '.join(tag.name for tag in self.tags)

    @property
    def tease(self):
        return self.body[:30]


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    slug = db.Column(db.String(30), unique=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def __repr__(self):
        return '<Tag: {}>'.format(self.name)


@login_manager.user_loader
def _user_loader(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(255))
    slug = db.Column(db.String(64), unique=True)
    active = db.Column(db.Boolean, default=True)
    admin = db.Column(db.Boolean, default=False)
    created_timestamp = db.Column(db.DateTime, default=datetime.now())
    entries = db.relationship('Entry', backref='author', lazy='dynamic')

    @staticmethod
    def make_password(plaintext):
        return bcrypt.generate_password_hash(plaintext)

    def check_password(self, raw_password):
        return bcrypt.check_password_hash(self.password_hash, raw_password)

    @classmethod
    def create(cls, email, password, **kwargs):
        return User(email=email, password_hash=User.make_password(password), **kwargs)

    @staticmethod
    def authenticate(email, password):
        user = User.query.filter(User.email == email).first()
        if user and user.check_password(raw_password=password):
            return user
        return False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.name:
            self.slug = slugify(self.name)

    def is_active(self):
        return self.active

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def __repr__(self):
        return "<User: {}>".format(self.email)

    def is_admin(self):
        return self.admin


class Comment(db.Model):
    __tablename__ = 'comments'
    STATUS_PEDNING_MODERATION = 0
    STATUS_PUBLIC = 1
    STATUS_SPAM = 8
    STATUS_DELETED = 9

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    ip_address = db.Column(db.String(64))
    url = db.Column(db.String(200))
    body = db.Column(db.Text)
    status = db.Column(db.SmallInteger)
    created_timestamp = db.Column(db.DateTime, default=datetime.now())
    entry_id = db.Column(db.Integer, db.ForeignKey('entries.id'))

    def __repr__(self):
        return '<Comment: {}>'.format(self.name)
