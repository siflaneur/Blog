# coding=utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

from blog.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me?', default=False)
    submit = SubmitField('Submit')

    def validate_on_submit(self):
        if not super().validate():
            return False
        self.user = User.authenticate(self.email.data, self.password.data)
        if not self.user:
            self.email.errors.append('Invalid email or password')
            return False
        return True
