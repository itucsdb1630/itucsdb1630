from imdbpie import Imdb
from requests.exceptions import HTTPError
from lightmdb.models import Movie
from lightmdb.utils import search_video

"""
IMDB Search Plugin.
@author Emre Eroglu
@author Emin Mastizada
"""

def search_movie(movie_name):
    imdb = Imdb()
    return imdb.search_for_title(movie_name)


def get_movie(imdb_id):
    imdb = Imdb()
    try:
        return imdb.get_title_by_id(imdb_id)
    except HTTPError as e:
        return None


def search_person(person_name):
    imdb = Imdb()
    return imdb.search_for_person(person_name)


def get_person(imdb_id):
    imdb = Imdb()
    try:
        return imdb.get_person_by_id(imdb_id)
    except HTTPError as e:
        return None


def save_movie(pk):
    imdb_movie = get_movie(pk)
    if not imdb_movie:
        return None
    video = search_video(imdb_movie.title, count=1)
    if not len(video):
        video = [None]
    movie_plot = ""
    for plot in imdb_movie.plots:
        movie_plot += "<p>" + plot + "</p>"
    movie = Movie(
        title=imdb_movie.title,
        synopsis=imdb_movie.plot_outline,
        plot=movie_plot,
        year=imdb_movie.year,
        cover=imdb_movie.cover_url,
        trailer=video[0],
        certification=imdb_movie.certification,
        runtime=imdb_movie.runtime,
        imdb_pk=pk,
        imdb_score=imdb_movie.rating
    )
    movie = movie.save()
    return movie.pk
