# coding=utf-8
import os

from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from app import app, db
from entries.form import EntryForm, ImageForm
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
    if request.method == 'POST' and form.validate_on_submit():
        entry = form.save_entry(Entry())
        db.session.add(entry)
        db.session.commit()
        flash('Enrty {} has been created successfully'.format(entry.title), 'success')
        return redirect(url_for('.detail', slug=entry.slug))
    return render_template('entries/create.html', form=form)


@entries.route('/<slug>/edit', methods=['GET', 'POST'])
def edit(slug):
    form = EntryForm()
    entry = Entry.query.filter(Entry.slug == slug).first_or_404()
    if request.method == 'POST' and form.validate_on_submit():
        entry = form.save_entry(entry)
        db.session.add(entry)
        db.session.commit()
        flash('Enrty {} has been saved'.format(entry.title), 'success')
        return redirect(url_for('.detail', slug=entry.slug))
    return render_template('entries/edit.html', form=form, entry=entry)


@entries.route('/<slug>/delete', methods=['GET', 'POST'])
def delete(slug):
    entry = Entry.query.filter(Entry.slug == slug).first_or_404()
    if request.method == "POST":
        entry.status = Entry.STATUS_DELETED
        db.session.add(entry)
        db.session.commit()
        flash('Enrty {} has been created deleted'.format(entry.title), 'success')
        return redirect(url_for('.index'))
    return render_template('entries/delete.html', entry=entry)


@entries.route('/image-upload/', methods=['GET', 'POST'])
def upload():
    form = ImageForm()
    if request.method == 'POST' and form.validate_on_submit():
        image_file = request.files['file']
        filename = os.path.join(app.config['IMAGES_DIR'], secure_filename(image_file.filename))
        image_file.save(filename)
        flash('Saved {}'.format(os.path.basename(filename), 'success'))
        return redirect(url_for('entries.index'))
    return render_template('entries/image_upload.html', form=form)
