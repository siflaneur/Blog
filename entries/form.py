# coding=utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import Length, Email, DataRequired

from models import Entry


class EntryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    status = SelectField('Entry status', choices=((Entry.STATUS_PUBLIC, 'Public'),
                                                  (Entry.STATUS_DRAFT, 'Draft')), coerce=int)
    create = SubmitField('Create')

    def save_entry(self, entry):
        self.populate_obj(entry)
        entry.generate_slug()
        return entry
