from flask import current_app
from collections import OrderedDict

def get_database():
    from lightmdb import get_db
    return get_db(current_app)

class Movie(object):
    """Movie Model."""
    TABLE_NAME = 'movies'
    def __init__(self, pk=None, title=None, year=None, votes=None, rating=None,
                 rewatch=None,deleted=False):
        self.pk = pk
        self.title = title
        self.year = year
        self.votes = votes
        self.rating = rating
        self.rewatch = rewatch
        self.deleted = bool(deleted)

    @property
    def is_active(self):
        return not self.deleted

    def get_id(self):
        return str(self.pk)

    def values(self):
        data = OrderedDict([
            ('pk', self.pk),
            ('title', self.title),
            ('year', self.year),
            ('votes', self.votes),
            ('rating', self.rating),
            ('rewatch', self.rewatch),
            ('deleted', self.deleted),
        ])
        return data

    @classmethod
    def get(cls, pk=None, title=None, year=None):
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
        elif title:
            cursor.execute(
                "SELECT * FROM {table} WHERE title=%(title)s".format(table=cls.TABLE_NAME),
                {'title': title}
            )
        elif year:
            cursor.execute(
                "SELECT * FROM {table} WHERE year=%(year)s".format(table=cls.TABLE_NAME),
                {'year': year}
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
        query = "SELECT * FROM " + cls.TABLE_NAME
        if kwargs:
            filter_query, filter_data = db.where_builder(kwargs)
            query += " WHERE " + filter_query
        cursor = db.cursor
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
        query = "UPDATE {table} SET deleted = TRUE WHERE id=%(id)s".format(table=self.TABLE_NAME)
        cursor.execute(query, {'id': self.pk})
        db.commit()

    def save(self):
        db = get_database()
        data = self.values()
        movie = self.get(title=self.title)
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
                "(title, year, votes, rating, rewatch) " \
                "VALUES" \
                "(%(title)s, %(year)s, %(votes)s, %(rating)s, " \
                "%(rewatch)s)".format(table=self.TABLE_NAME)
        db.cursor.execute(query, dict(data))
        db.commit()
        return self.get(title=self.title)
