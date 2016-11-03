from flask import Blueprint, render_template, current_app, flash, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from lightmdb.forms import LoginForm, UserForm, MovieForm
from lightmdb.models import User, Movie

from datetime import datetime

frontend = Blueprint('frontend', __name__)


@frontend.route("/")
def index():
    now = datetime.now()
    return render_template('index.html', current_time=now.ctime())


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

@frontend.route("/register/", methods=["GET", "POST"])
def register():
    form = MovieForm(request.form)
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



@frontend.route("/contactus/", methods=["GET", "POST"])
def contact_us():
    form = ContactForm(request.form)
    if request.method == 'POST' and form.validate():
        message = ContactMessage(
            title=form.title.data,
            content=form.content.data,
            email=form.email.data,
            phone=form.phone.data
        )
        message.save()
        return redirect(url_for('.contact_us'))
    return render_template('contactus.html', form=form)

@frontend.route("/admin/contactus/", methods=["GET", "POST"])
def contact_us_admin():
    desired_types = ['new']
    if request.method == 'POST':
        flash(request.form)
        if 'update' in request.form and 'status' in request.form:
            message=ContactMessage(request.form['update'])
            message.change_status(request.form['status'])
        elif 'delete' in request.form:
            message = ContactMessage(request.form['delete'])
            message.delete_message()
        elif 'show' in request.form:
            desired_types=[]
            all_types=['new','replied','waiting','spam','closed']
            for one_type in all_types:
                if one_type in request.form:
                    desired_types.append(one_type)
    messages=ContactMessage.get_messages(desired_types)
    return render_template('contactusadmin.html', table=messages,thead=['Update Status','Title','Content','Email','Phone','Status','Sent Time','Delete'])


@frontend.route("/logout/", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('.index'))


@frontend.route("/initdb/", methods=["GET"])
def initdb():
    """Temporary method to flush database."""
    from lightmdb import init_db
    if current_user.is_authenticated:
        logout_user()
    init_db(current_app)
    user = User.get(username='admin')
    user.set_password('admin')
    user = user.save()
    return redirect(url_for('.index'))


@frontend.route("/playlist")
def playlist():
    now = datetime.now()
    return render_template('playlist.html', current_time=now.ctime())


@frontend.route("/privacypolicy/")
def privacy():
    return render_template('privacy.html')


@frontend.route("/toplists/")
def toplists():
    return render_template('toplists.html')
