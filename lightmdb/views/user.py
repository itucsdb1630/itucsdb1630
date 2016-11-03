from flask import Blueprint, abort, request, render_template
from flask_login import login_required, current_user
from lightmdb.models import User
from lightmdb.forms import UserForm

user = Blueprint('user', __name__)


@user.route("/<username>")
@login_required
def profile(username):
    user = User.get(username=username)
    if not user:
        abort(404, {'message': "User not found."})
    return render_template('user/profile.html', user=user)


@user.route("/me")
@login_required
def me():
    return profile(current_user.username)
