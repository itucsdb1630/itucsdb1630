from flask import Blueprint, render_template, current_app, request

playlist = Blueprint('playlists', __name__)


@playlist.route("/")
def playlists():
    return render_template('playlist/playlist.html')


@playlist.teardown_request
def close_connection(error=None):
    from lightmdb import close_db
    close_db()
