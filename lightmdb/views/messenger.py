from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, logout_user, current_user
from lightmdb.models import Messenger, User

messenger = Blueprint('messenger', __name__)


@messenger.route("/logout/", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('frontend.logout'))


@messenger.route("/")
@login_required
def main():
    user_list = current_user.friendlist
    messages = Messenger.get(sender_pk=current_user.pk, receiver_pk=current_user.pk)
    return render_template('messenger/messenger.html', user_list=user_list, messages=messages, receiver=current_user)


@messenger.route("/getmessages/<pk>/", methods=["GET", "POST"])
@login_required
def get_messages(pk):
    messages = Messenger.get(sender_pk=current_user.pk, receiver_pk=pk)
    user_list = current_user.friendlist
    receiver = User.get(pk=pk)
    return render_template('messenger/messenger.html', user_list=user_list, messages=messages, receiver=receiver)


@messenger.route("/sendmessage/<pk>/", methods=["GET", "POST"])
@login_required
def send_message(pk):
    message = request.form.get("message", "")
    message = Messenger(sender_pk=current_user.pk, receiver_pk=pk, message=message)
    message.save()
    messages = Messenger.get(sender_pk=current_user.pk, receiver_pk=pk)
    user_list = current_user.friendlist
    receiver = User.get(pk=pk)
    return render_template('messenger/messenger.html', user_list=user_list, messages=messages, receiver=receiver)


@messenger.route("/deletemessage/<pk>/<message_pk>/", methods=["GET", "POST"])
@login_required
def delete_message(message_pk, pk):
    Messenger.__delete__(message_pk)
    messages = Messenger.get(sender_pk=current_user.pk, receiver_pk=pk)
    user_list = current_user.friendlist
    receiver = User.get(pk=pk)
    return render_template('messenger/messenger.html', user_list=user_list, messages=messages, receiver=receiver)


@messenger.teardown_request
def close_connection(error=None):
    from lightmdb import close_db
    close_db()
