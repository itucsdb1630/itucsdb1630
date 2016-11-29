from flask import Blueprint, abort, request, render_template, redirect, url_for
from flask_login import login_required, current_user
from lightmdb.models import User
from lightmdb.forms import ProfileForm

user = Blueprint('user', __name__)


@user.route("/<username>")
@login_required
def profile(username):
    _user = User.get(username=username)
    if not _user:
        abort(404, {'message': "User not found."})
    return render_template('user/profile.html', user=_user)


@user.route("/me")
@login_required
def me():
    return profile(current_user.username)


@user.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    if request.form:
        form = ProfileForm(request.form)
    else:
        form = ProfileForm(
            name=current_user.name,
            email=current_user.email
        )
    if request.method == 'POST' and form.validate():
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.save()
        return redirect(url_for('user.me'))
    return render_template('user/edit.html', form=form)


@user.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    if request.method == 'POST':
        current_user.delete()
        return redirect(url_for('frontend.logout'))
    return render_template('user/delete.html')
