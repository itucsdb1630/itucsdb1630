from flask import Blueprint, render_template, current_app, flash, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from lightmdb.models import User

admin = Blueprint('admin', __name__)


@admin.route("/")
def index():
    data = {}
    return render_template('admin/index.html', **data)

@admin.teardown_request
def close_connection(error=None):
    from lightmdb import close_db
    close_db()
