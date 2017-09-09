# coding=utf-8
from flask import Blueprint, render_template, request
from helpers import g_object_list
from models import Entry, Tag

entries = Blueprint('entries', __name__, template_folder='templates')


def entry_list(template, query, **content):
    search = request.args.get('q')
    if search:
        query = query.filter((Entry.body.contains(search)) |
                             (Entry.title.contains(search)))
    return g_object_list(template, query, **content)


@entries.route('/')
def index():
    get_entries = Entry.query.order_by(Entry.created_timestamp.desc())
    return entry_list('entries/index.html', get_entries)


@entries.route('/tags/')
def tag_index():
    tags = Tag.query.order_by(Tag.name)
    return g_object_list('entries/tag_index.html', tags)


@entries.route('/tags/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    entries = tag.entries.order_by(Entry.created_timestamp.desc())
    return entry_list('entries/tag_detail.html', entries, tag=tag)


@entries.route('/<slug>')
def detail(slug):
    entry = Entry.query.filter(Entry.slug == slug).first()
    return render_template('entries/detail.html', entry=entry)
