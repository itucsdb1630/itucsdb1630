from flask import Blueprint, render_template, current_app, request, abort, redirect, url_for
from flask_login import login_required
from lightmdb.forms import MovieForm
from lightmdb.models import Movie

movies = Blueprint('movies', __name__)


@movies.route("/<pk>")
def movie(pk):
    _movie = Movie.get(pk)
    if not _movie:
        abort(404, {'message': 'Movie not found.'})
    return render_template('movie/movie.html', pk=pk,movie=_movie)

@movies.route("/update/<pk>", methods=["GET","POST"])
def update_movie(pk):
    _movie = Movie.get(pk)
    if not _movie:
        abort(404, {'message': 'Movie not found.'})
    form = MovieForm(request.form)
    if request.method == 'POST' and form.validate():
        _movie.title = form.title.data
        _movie.year = form.year.data
        _movie.synopsis = form.synopsis.data
        _movie.save()
        return render_template('movie/movie.html', pk=pk,movie=_movie)
    return render_template('movie/update.html', form=form,movie=_movie)

@login_required
@movies.route("/new/", methods=["GET", "POST"])
def add_movie():
    form = MovieForm(request.form)
    if request.method == 'POST' and form.validate():
        # @TODO Check if movie with same title exists
        _movie = Movie(title=form.title.data, year=form.year.data, synopsis=form.synopsis.data)
        _movie = _movie.save()
        return redirect(url_for('.movie', pk=_movie.pk))
    return render_template('movie/add.html', form=form)
