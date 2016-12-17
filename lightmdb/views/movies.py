from flask import Blueprint, flash, render_template, current_app, request, abort, redirect, url_for
from flask_login import login_required
from lightmdb.forms import MovieForm, UpdateMovieForm
from lightmdb.models import Movie
from lightmdb.utils import search_movie, get_movie, save_movie


movies = Blueprint('movies', __name__)


@movies.route("/<pk>")
def movie(pk):
    if 'tt' in pk:
        _movie = Movie.get(imdb_pk=pk)
        if not _movie:
            pk = save_movie(pk)
            if not pk:
                abort(404, {'message': "Movie cannot be saved."})
            return redirect(url_for('.movie', pk=pk))
        return redirect(url_for('.movie', pk=_movie.pk))
    _movie = Movie.get(pk)
    if not _movie:
        abort(404, {'message': 'Movie not found.'})
    return render_template('movie/movie.html', pk=pk,movie=_movie)


@movies.route("/update/<pk>", methods=["GET","POST"])
@login_required
def update_movie(pk):
    _movie = Movie.get(pk)
    if not _movie:
        abort(404, {'message': 'Movie not found.'})
    if request.form:
        form = UpdateMovieForm(request.form)
    else:
        form = UpdateMovieForm(
            pk=_movie.pk,
            title=_movie.title,
            year=_movie.year,
            synopsis=_movie.synopsis
        )
    if request.method == 'POST' and form.validate():
        _movie.title = form.title.data
        _movie.year = form.year.data
        _movie.synopsis = form.synopsis.data
        _movie.save()
        return redirect(url_for('.movie', pk=pk))
    data = {'form': form, 'movie': _movie}
    return render_template('movie/update.html', **data)


@movies.route("/delete/<pk>", methods=["GET","POST"])
@login_required
def delete_movie(pk):
    _movie = Movie.get(pk)
    if not _movie:
        abort(404, {'message': 'Movie not found.'})
    _movie.delete()
    flash("Movie deleted!")
    return redirect("/")


@movies.route("/new/", methods=["GET", "POST"])
@login_required
def add_movie():
    form = MovieForm(request.form)
    if request.method == 'POST' and form.validate():
        # @TODO Check if movie with same title exists
        _movie = Movie(title=form.title.data, year=form.year.data, synopsis=form.synopsis.data)
        _movie = _movie.save()
        return redirect(url_for('.movie', pk=_movie.pk))
    return render_template('movie/add.html', form=form)


@movies.route("/search/")
def search():
    query = request.args.get('q')
    provider_result = search_movie(query)[:5]
    movies = []
    for movie in provider_result:
        movies.append(get_movie(movie['imdb_id']))
    print(movies)
    data = {'movies': movies}
    return render_template('movie/search.html', **data)


@movies.teardown_request
def close_connection(error=None):
    from lightmdb import close_db
    close_db()
