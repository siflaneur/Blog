# coding=utf-8
import os

from flask import abort, Blueprint, flash, g, redirect, render_template, request, url_for
from flask_login import LoginManager, login_required
from werkzeug.utils import secure_filename

from blog.app import app, db
from blog.entries.form import EntryForm, ImageForm
from blog.helpers import g_object_list
from blog.models import Entry, Tag

entries = Blueprint('entries', __name__, template_folder='./templates')


def entry_list(template, query, **content):
    """
    Do the query and delegate the variable query to g_object_list().
    if body or title contain the word you typed in query box or URI,
    then you will see the result in the response page.
    """
    query = filter_status_by_user(query)

    valid_status = [Entry.STATUS_PUBLIC, Entry.STATUS_DRAFT]
    query = query.filter(Entry.status.in_(valid_status))
    if request.args.get('q'):
        search = request.args.get('q')
        query = query.filter(
            (Entry.body.contains(search)) |
            (Entry.title.contains(search))
        )
    return g_object_list(template, query, **content)


def filter_status_by_user(query):
    if not g.user.is_authenticated:
        return query.filter(Entry.status == Entry.STATUS_PUBLIC)
    else:
        query = query.filter(
            (Entry.status == Entry.STATUS_PUBLIC) |
            ((Entry.author == g.user) &
             (Entry.status != Entry.STATUS_DELETED)))
    return query


def get_entry_or_404(slug, author=None):
    query = Entry.query.filter(Entry.slug == slug)
    if author:
        query = query.filter(Entry.author == author)
    else:
        query = filter_status_by_user(query)
    return query.first_or_404()


@entries.route('/')
def index():
    get_entries = Entry.query.order_by(Entry.created_timestamp.desc())
    return entry_list('entries/index.html', get_entries)


@entries.route('/tags/')
def tag_index():
    tags = Tag.query.order_by(Tag.name)
    if tags:
        return g_object_list('entries/tag_index.html', tags)
    abort(404)


@entries.route('/tags/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    if tag:
        entries = tag.entries.order_by(Entry.created_timestamp.desc())
        return entry_list('entries/tag_detail.html', entries, tag=tag)
    abort(404)


@entries.route('/<slug>')
def detail(slug):
    entry = Entry.query.filter(Entry.slug == slug).first()
    if entry:
        return render_template('entries/detail.html', entry=entry)
    abort(404)


@entries.route('/create/', methods=['POST', 'GET'])
@login_required
def create():
    form = EntryForm()
    if request.method == 'POST' and form.validate_on_submit():
        entry = form.save_entry(Entry(author=g.user))
        db.session.add(entry)
        db.session.commit()
        flash('Enrty {} has been created successfully'.format(entry.title), 'success')
        return redirect(url_for('.detail', slug=entry.slug))
    return render_template('entries/create.html', form=form)


@entries.route('/<slug>/edit', methods=['GET', 'POST'])
@login_required
def edit(slug):
    form = EntryForm()
    entry = get_entry_or_404(slug, author=None)
    if request.method == 'POST' and form.validate_on_submit():
        entry = form.save_entry(entry)
        db.session.add(entry)
        db.session.commit()
        flash('Enrty {} has been saved'.format(entry.title), 'success')
        return redirect(url_for('.detail', slug=entry.slug))
    return render_template('entries/edit.html', form=form, entry=entry)


@entries.route('/<slug>/delete', methods=['GET', 'POST'])
@login_required
def delete(slug):
    entry = get_entry_or_404(slug, author=None)
    if request.method == "POST":
        entry.status = Entry.STATUS_DELETED
        db.session.add(entry)
        db.session.commit()
        flash('Enrty {} has been created deleted'.format(entry.title), 'success')
        return redirect(url_for('.index'))
    return render_template('entries/delete.html', entry=entry)


@entries.route('/image-upload/', methods=['GET', 'POST'])
@login_required
def upload():
    form = ImageForm()
    if request.method == 'POST' and form.validate_on_submit():
        image_file = request.files['file']
        filename = os.path.join(app.config['IMAGES_DIR'], secure_filename(image_file.filename))
        image_file.save(filename)
        flash('Saved {}'.format(os.path.basename(filename), 'success'))
        return redirect(url_for('entries.index'))
    return render_template('entries/image_upload.html', form=form)
