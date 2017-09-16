# coding=utf-8
from flask import request
from flask_wtf import FlaskForm
from wtforms import FileField, StringField, SelectField, SubmitField, TextAreaField
from wtforms.validators import Length, Email, DataRequired, ValidationError

from blog.models import Entry, Tag


class TagField(StringField):
    def _value(self):
        if self.data:
            return ', '.join([tag.name for tag in self.data])
        return ''

    @classmethod
    def get_tag_from_string(cls, tag_string):
        raw_tags = tag_string.split(',')
        tag = [tag.strip() for tag in raw_tags if tag.strip()]  # filter the empty string
        existing_tag = Tag.query.filter(Tag.name.in_(tag))  # Query the database for the tags we have
        new_names = set(tag) - set([tag.name for tag in existing_tag])
        new_tags = [Tag(name=name) for name in new_names]  # Create new tags for those are not in database
        return list(existing_tag) + new_tags

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = self.get_tag_from_string(valuelist[0])
        else:
            self.data = []


class EntryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    status = SelectField('Entry status', choices=((Entry.STATUS_PUBLIC, 'Public'),
                                                  (Entry.STATUS_DRAFT, 'Draft')), coerce=int)
    tags = TagField('Tags', description='Seperate multiple tags with commas')
    create = SubmitField('Create')

    def save_entry(self, entry):
        self.populate_obj(entry)
        entry.generate_slug()
        return entry


def check_image(form, field):
    file = request.files['file']
    filename = file.filename
    if not filename.endswith('.jpg'):
        raise ValidationError('Must be an image')


class ImageForm(FlaskForm):
    file = FileField('Image field', validators=[check_image])
    Upload = SubmitField('Upload')
