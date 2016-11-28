from flask import Blueprint, render_template, current_app, request
from datetime import datetime
from lightmdb.forms import MovieForm
from lightmdb.models import Movie

movies = Blueprint('movies', __name__)

@movies.route("/movie/<idnum>")
def movie(idnum):
	mov = Movie.get(idnum)
	if not mov:
		abort(404,{'message':'Movie not found.'})
	return render_template('movie/movie.html',pk=idnum)

@movies.route("/addmovie/", methods=["GET", "POST"])
def add_movie():
	if request.method == 'POST' and form.validate():
		form = MovieForm(request.form)
		mov = Movie(title=form.title.data,year=form.year.data)
		mov.save()
		return render_template("movie/added.html")
	return render_template('movie/addmovie.html',form=form)	
