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
    update_message = None
    return render_template('messenger/messenger.html', user_list=user_list, messages=messages, receiver=current_user, update_message=update_message)


@messenger.route("/getmessages/<pk>/", methods=["GET", "POST"])
@login_required
def get_messages(pk):
    messages = Messenger.get(sender_pk=current_user.pk, receiver_pk=pk)
    user_list = current_user.friendlist
    receiver = User.get(pk=pk)
    update_message = None
    return render_template('messenger/messenger.html', user_list=user_list, messages=messages, receiver=receiver, update_message=update_message)


@messenger.route("/sendmessage/<pk>/", methods=["GET", "POST"])
@login_required
def send_message(pk):
    message = request.form.get("message", "")
    message = Messenger(sender_pk=current_user.pk, receiver_pk=pk, message=message)
    message.save()
    messages = Messenger.get(sender_pk=current_user.pk, receiver_pk=pk)
    user_list = current_user.friendlist
    receiver = User.get(pk=pk)
    update_message = None
    return render_template('messenger/messenger.html', user_list=user_list, messages=messages, receiver=receiver, update_message=update_message)


@messenger.route("/updatedmessage/<pk>/<message_pk>/", methods=["GET", "POST"])
@login_required
def updated_message(pk, message_pk):
    new_message = request.form.get("message", "")
    update_message = Messenger.get(pk=message_pk)
    update_message.message = new_message
    update_message.save()
    messages = Messenger.get(sender_pk=current_user.pk, receiver_pk=pk)
    user_list = current_user.friendlist
    receiver = User.get(pk=pk)
    return render_template('messenger/messenger.html', user_list=user_list, messages=messages, receiver=receiver, update_message=update_message)


@messenger.route("/deletemessage/<pk>/<message_pk>/", methods=["GET", "POST"])
@login_required
def delete_message(message_pk, pk):
    Messenger.__delete__(message_pk)
    messages = Messenger.get(sender_pk=current_user.pk, receiver_pk=pk)
    user_list = current_user.friendlist
    receiver = User.get(pk=pk)
    update_message = None
    return render_template('messenger/messenger.html', user_list=user_list, messages=messages, receiver=receiver, update_message=update_message)


@messenger.route("/updatemessage/<pk>/<message_pk>/", methods=["GET", "POST"])
@login_required
def update_message(message_pk, pk):
    update_message = Messenger.get(pk=message_pk)
    messages = Messenger.get(sender_pk=current_user.pk, receiver_pk=pk)
    user_list = current_user.friendlist
    receiver = User.get(pk=pk)
    return render_template('messenger/messenger.html', message_pk=message_pk, user_list=user_list, messages=messages, receiver=receiver, update_message=update_message)


@messenger.teardown_request
def close_connection(error=None):
    from lightmdb import close_db
    close_db()
