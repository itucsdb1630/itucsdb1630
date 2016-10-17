from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_user
from lightmdb.forms import LoginForm
from lightmdb.models import User

from datetime import datetime


frontend = Blueprint('frontend', __name__)


@frontend.route("/")
def index():
    now = datetime.now()
    return render_template('home.html', current_time=now.ctime())

@frontend.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.get(username=form.username.data)
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully.')
            _next = request.args.get('next')
            if _next:
                return redirect(_next or url_for('index'))
        else:
            flash('Wronge credentials!')
    return render_template('login.html', form=form)
