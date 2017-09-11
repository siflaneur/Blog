# coding=utf-8
from flask import Blueprint, redirect, render_template, request, url_for

from app import db
from entries.form import EntryForm
from helpers import g_object_list
from models import Entry, Tag

entries = Blueprint('entries', __name__, template_folder='./templates')


def entry_list(template, query, **content):
    """
    Do the query and delegate the variable query to g_object_list().
    if body or title contain the word you typed in query box or URI,
    then you will see the result in the response page.
    """
    search = request.args.get('q')
    query = query.filter(Entry.status == 0)
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


@entries.route('/create/', methods=['POST', 'GET'])
def create():
    # form = EntryForm()
    form = EntryForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            entry = form.save_entry(Entry())
            db.session.add(entry)
            db.session.commit()
            return redirect(url_for('entries.detail', slug=entry.slug))
    return render_template('entries/create.html', form=form)
