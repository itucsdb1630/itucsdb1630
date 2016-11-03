from flask import Blueprint, render_template, current_app, flash, request, redirect, url_for
from datetime import datetime


toplist = Blueprint('toplist', __name__)


@toplist.route("/")
def toplists():
    return render_template('toplist/toplists.html')
