from flask import Blueprint
from flask import render_template
# from flask import request

from datetime import datetime


frontend = Blueprint('frontend', __name__)


@frontend.route("/")
def index():
    now = datetime.now()
    return render_template('home.html', current_time=now.ctime())
