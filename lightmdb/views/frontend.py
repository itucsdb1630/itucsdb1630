from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from lightmdb.forms import LoginForm, UserForm
from lightmdb.models import User

from datetime import datetime

frontend = Blueprint('frontend', __name__)


@frontend.route("/")
def index():
    now = datetime.now()
    return render_template('index.html', current_time=now.ctime())

@frontend.route("/playlist")
def playlist():
    now = datetime.now()
    return render_template('playlist.html', current_time=now.ctime())

@frontend.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.get(username=form.username.data)
        if user and user.check_password(form.password.data):
            login_status = login_user(user)
            if not login_status:
                return render_template('user/login.html', form=form, errors="User Disabled, Contact Support!")
            flash('Logged in successfully.')
            _next = request.args.get('next')
            if _next:
                return redirect(_next or url_for('.index'))
        else:
            return render_template('user/login.html', form=form, errors="Wronge Credentials")
    return render_template('user/login.html', form=form)


@frontend.route("/register/", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('.index'))
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate():
        # @TODO Check if user with same email or username exists
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            name=form.name.data
        )
        user = user.save()
        # @TODO Use confirmation email
        login_user(user)
        return redirect(url_for('.index'))
    return render_template('user/register.html', form=form)


@frontend.route("/logout/", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('.index'))



