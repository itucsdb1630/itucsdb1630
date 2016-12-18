from flask import Blueprint, flash, render_template, current_app, request, abort, redirect, url_for
from flask_login import login_required
from lightmdb.forms import MovieForm, UpdateMovieForm
from lightmdb.models import Movie
from lightmdb.utils import search_movie, get_movie, save_movie


movies = Blueprint('movies', __name__)


@movies.route("/<pk>",methods=['POST','GET'])
def movie(pk):
    tags=[]
    tagedit=False
    movie_tags=[]
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
    else:
        if request.method == 'POST':
            if 'saver' in request.form:
                if 'tag' in request.form and request.form['tag'] !='0':
                    new_movie_tag=MovieTags(tag_id=request.form['tag'],movie_id=pk)
                    new_movie_tag.save()
                if 'tag' in request.form and request.form['tag'] =='0' and 'newtag' in request.form and len(request.form['newtag'])>0 :
                    new_tag=Tag(tag_name=request.form['newtag'])
                    new_tag.save()
                    tag=new_tag.get_tag_by_name()
                    tag_id=tag[0]
                    new_movie_tag = MovieTags(tag_id=tag_id, movie_id=pk)
                    new_movie_tag.save()
            elif 'deltag' in request.form:
                movie_tag=MovieTags(movie_tag_id=request.form['deltag'])
                movie_tag.delete()
            elif 'edittags' in request.form:
                tagedit=True
            elif 'tagedited' in request.form:
                tag_id=request.form['tagedited']
                tag = Tag(tag_id=tag_id)
                tag.update_name(request.form[tag_id])
            elif 'tagdelete' in request.form:
                tag_id=request.form['tagdelete']
                tag = Tag(tag_id=tag_id)
                MovieTags.delete_by_tag_id(tag_id)
                tag.delete()
        tags = Tag.get_tags()
        movietag = MovieTags(movie_id=pk)
        movie_tags =movietag.get_movie_tags_by_movie_id()


    return render_template('movie/movie.html', pk=pk,movie=_movie,tags=tags,movie_tags=movie_tags,tagedit=tagedit)



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
    if not query or not len(query):
        return redirect(url_for('frontend.index'))
    provider_result = search_movie(query)[:5]
    movies = []
    for movie in provider_result:
        movies.append(get_movie(movie['imdb_id']))
    data = {'movies': movies}
    return render_template('movie/search.html', **data)


@movies.teardown_request
def close_connection(error=None):
    from lightmdb import close_db
    close_db()
