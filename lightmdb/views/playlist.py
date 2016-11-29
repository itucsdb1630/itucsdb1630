from flask import Blueprint, render_template, current_app, request
from datetime import datetime

playlist = Blueprint('playlist', __name__)


@playlist.route("/new/", methods = ["GET","POST"])
@login_required
def add_playlist():
    form = PlaylistForm(request.form)
    if request.method = 'POST' and form.validate():
        _playlist = Playlist(name=form.name.data,
        _playlist = _playlist.save(
        return redirect(url_for('.playlists',pk=_playlist.pk))
    return render_template('playlist/add.html')

@playlist.route("/<pk>",methods = ["GET","POST"])
def playlists(pk):
    _playlist = Playlist.get(pk)
    if not _playlist:
        abort(404,{'message':'Playlist not found.'})
	_movies = _playlist.get_movies()
    return render_template('playlist/playlist.html',movies = _movies, playlist = _playlist)

