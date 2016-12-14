from flask import Blueprint, abort, request, render_template, redirect, url_for, jsonify
from flask_login import login_required, current_user
from lightmdb.models import User, Follower
from lightmdb.forms import ProfileForm

user = Blueprint('user', __name__)


@user.route("/<username>")
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


@user.route("/follow/<pk>/", methods=["POST"])
@login_required
def follow(pk):
    """Json view for following.

    201: Followed
    202: Already following
    403: Follow not allowed
    404: User not found
    """
    if current_user.pk == pk:
        # Trying to follow self? So lonely?
        response = jsonify({'code': 403, 'message': 'Following self not allowed'})
        response.status_code = 403
        return response
    following_user = User.get(pk=pk)
    if not following_user:
        response = jsonify({'code': 404, 'message': 'User not found'})
        response.status_code = 404
        return response
    if Follower.get(follower_id=current_user.pk, following_id=pk):
        response = jsonify({'code': 202, 'message': 'Already following'})
        response.status_code = 202
        return response
    follow_data = Follower(follower_id=current_user.pk, following_id=pk)
    follow_data.save()
    response = jsonify({'code': 201, 'message': 'Followed'})
    response.status_code = 201
    return response


@user.route("/unfollow/<pk>/", methods=["POST"])
@login_required
def unfollow(pk):
    """Json view for unfollowing."""
    follow_data = Follower.get(follower_id=current_user.pk, following_id=pk)
    if not follow_data:
        response = jsonify({'code': 202, 'message': 'Already unfollowed'})
        response.status_code = 202
        return response
    follow_data.delete()
    response = jsonify({'code': 201, 'message': 'Unfollowed'})
    response.status_code = 201
    return response


# Context Processors for template
@user.context_processor
def user_details():
    def is_following(pk):
        return current_user.is_following(pk)
    return dict(is_following=is_following)


@user.teardown_request
def close_connection(error=None):
    from lightmdb import close_db
    close_db()
