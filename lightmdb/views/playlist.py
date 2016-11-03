from flask import Blueprint, render_template, current_app, request
from datetime import datetime

playlist = Blueprint('playlists', __name__)


@playlist.route("/")
def playlists():
    return render_template('playlist/playlist.html')
