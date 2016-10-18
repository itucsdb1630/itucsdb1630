from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, logout_user


messenger = Blueprint('messenger', __name__)



@messenger.route("/logout/", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('frontend.logout'))


@messenger.route("/")
@login_required
def main():
    return render_template('messenger/messenger.html')
