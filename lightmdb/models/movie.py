from flask import current_app
from collections import OrderedDict


def get_database():
    from lightmdb import get_db
    return get_db(current_app)


class Movie(object):
    """Movie Model."""
    TABLE_NAME = 'movies'

    def __init__(self, pk=None, title=None, synopsis=None, plot=None, year=None, runtime=None, votes=0, score=0,
                 rewatchability_count=0, rewatchability=0, cover=None, trailer=None, certification=None,
                 imdb_pk=None, imdb_score=0):
        self.pk = pk
        self.title = title
        self.synopsis = synopsis
        self.plot = plot
        self.year = year
        self.runtime = runtime
        self.votes = votes
        self.score = score
        self.rewatchability_count = rewatchability_count
        self.rewatchability = rewatchability
        self.cover = cover
        self.trailer = trailer
        self.certification = certification
        self.imdb_pk = imdb_pk
        self.imdb_score = imdb_score

    def get_id(self):
        return str(self.pk)

    def values(self):
        data = OrderedDict([
            ('pk', self.pk),
            ('title', self.title),
            ('synopsis', self.synopsis),
            ('plot', self.plot),
            ('year', self.year),
            ('runtime', self.runtime),
            ('votes', self.votes),
            ('score', self.score),
            ('rewatchability_count', self.rewatchability_count),
            ('rewatchability', self.rewatchability),
            ('cover', self.cover),
            ('trailer', self.trailer),
            ('certification', self.certification),
            ('imdb_pk', self.imdb_pk),
            ('imdb_score', self.imdb_score),
        ])
        return data

    @classmethod
    def get(cls, pk=None, imdb_pk=None):
        """Get movie by identifier.

        Usage: Movie.get(title)
        :rtype: Movie object or None
        """
        db = get_database()
        cursor = db.cursor
        if pk:
            cursor.execute(
                "SELECT * FROM {table} WHERE id=%(id)s".format(table=cls.TABLE_NAME),
                {'id': pk}
            )
        elif imdb_pk:
            cursor.execute(
                "SELECT * FROM {table} WHERE imdb_pk=%(imdb_pk)s".format(table=cls.TABLE_NAME),
                {'imdb_pk': imdb_pk}
            )
        else:
            return None
        movie = db.fetch_execution(cursor)
        if movie:
            return Movie(**movie[0])
        return None

    @classmethod
    def filter(cls, **kwargs):
        db = get_database()
        cursor = db.cursor
        filter_data = {}
        query = "SELECT * FROM " + cls.TABLE_NAME
        if kwargs:
            filter_query, filter_data = db.where_builder(kwargs)
            query += " WHERE " + filter_query
        cursor.execute(query, filter_data)
        movies = db.fetch_execution(cursor)
        result = []
        for movie in movies:
            result.append(Movie(**movie))
        return result

    def delete(self):
        if not self.pk:
            raise ValueError("Movie is not saved yet.")
        db = get_database()
        cursor = db.cursor
        query = "DELETE FROM {table} WHERE id=%(id)s".format(table=self.TABLE_NAME)
        cursor.execute(query, {'id': self.pk})
        db.commit()

    def save(self, return_obj=True):
        db = get_database()
        data = self.values()
        movie = None
        if self.pk:
            movie = self.get(pk=self.pk)
        if movie:
            # update old movie
            old_data = movie.values()
            diffkeys = [key for key in data if data[key] != old_data[key]]
            if not diffkeys:
                # Nothing changed
                return movie
            filters = {}
            for key in diffkeys:
                filters[key] = self.values()[key]
            query = "UPDATE {table} SET ".format(table=self.TABLE_NAME)
            for key in filters:
                query += key + ' = %(' + key + ')s, '
            # Remove last comma
            query = query.rstrip(', ') + ' '
            # Add filter
            query += "WHERE id={pk}".format(pk=movie.pk)
            db.cursor.execute(query, filters)
            db.commit()
            # Return saved movie
            return self.get(pk=movie.pk)
        # new movie
        del data['pk']
        query = "INSERT INTO {table} " \
                "(title, synopsis, plot, year, runtime, votes, score, rewatchability_count, rewatchability, " \
                "cover, trailer, certification, imdb_pk, imdb_score) VALUES" \
                "(%(title)s, %(synopsis)s, %(plot)s, %(year)s, %(runtime)s, %(votes)s, %(score)s, " \
                "%(rewatchability_count)s, %(rewatchability)s, %(cover)s, %(trailer)s, %(certification)s, " \
                "%(imdb_pk)s, %(imdb_score)s)".format(table=self.TABLE_NAME)
        if return_obj:
            query += " RETURNING id"
        cursor = db.cursor
        cursor.execute(query, dict(data))
        if return_obj:
            new_row_pk = cursor.fetchone()[0]
            return self.get(pk=new_row_pk)
        # db.commit()
        return True

    @classmethod
    def top_movies(cls, limit=100, **kwargs):
        db = get_database()
        cursor = db.cursor
        filter_data = {}
        query = "SELECT * FROM " + cls.TABLE_NAME
        if kwargs:
            filter_query, filter_data = db.where_builder(kwargs)
            query += " WHERE " + filter_query
        query += " ORDER BY score DESC, imdb_score DESC "
        query += " LIMIT " + str(limit)
        cursor.execute(query, filter_data)
        movies = db.fetch_execution(cursor)
        result = []
        for movie in movies:
            result.append(Movie(**movie))
        return result
