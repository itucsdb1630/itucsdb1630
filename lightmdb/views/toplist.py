from flask import Blueprint, render_template, current_app, flash, request, redirect, url_for

toplist = Blueprint('toplist', __name__)


@toplist.route("/")
def toplists():
    return render_template('toplist/toplists.html')


@toplist.teardown_request
def close_connection(error=None):
    from lightmdb import close_db
    close_db()
