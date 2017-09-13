# coding=utf-8
from flask import flash, render_template, request, redirect, url_for
from flask_login import login_user

from app import app, login_manager
from form import LoginForm


@app.route('/')
def homepage():
    name = request.args.get('name')
    number = request.args.get('number')
    return render_template('homepage.html', name=name, number=number)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        login_user(form.user, remember=form.remember_me.data)
        flash('Successfully login in as {}'.format(form.email.data), 'success')
        return redirect(request.args.get('next') or url_for('homepage'))
    return render_template('login.html', form=form)
