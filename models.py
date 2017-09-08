# coding=utf-8
import re
from datetime import datetime

from app import db


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


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    slug = db.Column(db.String(100), unique=True)
    body = db.Column(db.Text)
    created_timestamp = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.SmallInteger, default=STATUS_PUBLIC)
    modified_timestamp = db.Column(db.DateTime,
                                   default=datetime.now,
                                   onupdate=datetime.now)
    tags = db.relationship('Tag', secondary=entry_tags,
                           backref=db.backref('entries', lazy='dynamic'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        self.slug = ''
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return '<Entry: {}>'.format(self.title)


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
