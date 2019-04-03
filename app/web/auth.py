# -*- coding:utf-8 -*-
# @Time : 4/1/19 3:13 PM
# @Author : zbz
from flask import request, redirect, url_for, render_template, flash
from flask_login import login_user

from app.form.auth import RegisterForm, LoginForm
from app.models.base import db
from app.models.user import User
from app.web import web


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            db.session.add(user)
        return redirect(url_for('web.login'))
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            next = request.args.get('next')
            if not next or not next.startswith('/'):
                next = url_for('web.annotation')
            return redirect(next)
        else:
            flash('帐号不存在或密码不正确')
    return render_template('auth/login.html', form=form)

@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    pass