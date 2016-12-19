from flask import Blueprint,flash, abort, redirect, url_for, render_template, current_app, request
from flask_login import login_required, current_user
from lightmdb.models import Playlist
from lightmdb.forms import PlaylistForm
from flask import Blueprint, render_template, current_app, request
from lightmdb.models import Playlist, Playlist_Movie

playlist = Blueprint('playlist', __name__)

@playlist.route("/new/", methods = ["GET","POST"])
@login_required
def add_playlist():
    form = PlaylistForm(request.form)
    if request.method == 'POST' and form.validate():
        is_public = False
        if form.privacy.data == "Public":
           is_public = True
        _playlist = Playlist(name=form.name.data,user_id=current_user.pk,is_public = is_public)
        _playlist = _playlist.save()
        return redirect(url_for('.playlists', pk=_playlist.pk))
    return render_template('playlist/add.html',form=form)


@playlist.route("/<pk>/",methods = ["GET","POST"])
def playlists(pk):
    _playlist = Playlist.get(pk)
    if not _playlist:
        abort(404,{'message':'Playlist not found.'})
    if _playlist:
        _movies = Playlist_Movie.get_by_playlist(_playlist.pk)
    return render_template('playlist/playlist.html', movies = _movies, playlist = _playlist)


@playlist.route("/delete/<pk>", methods=["GET","POST"])
@login_required
def delete_movie(pk):
    _playlist = Playlist.get(pk)
    if not _playlist:
        abort(404, {'message': 'Movie not found.'})
    _playlist.delete()
    flash("Movie deleted!")
    return redirect("/")

@playlist.route("/remove/<pk>/<m_pk>", methods=["GET","POST"])
@login_required
def remove_movie(pk,m_pk):
    _playlist_movie = Playlist_Movie.get_by_list_movie(pk,m_pk)
    if not _playlist_movie:
        abort(404, {'message': 'Movie not found.'})
        _playlist_movie.delete()
    flash("Movie deleted!")
    return redirect("/")


@playlist.route("/")
def playlists_index():
    _playlists = Playlist.get_all()
    return render_template('playlist/playlists.html',plists=_playlists)


@playlist.teardown_request
def close_connection(error=None):
    from lightmdb import close_db
    close_db()
