from flask import current_app
from collections import OrderedDict


def get_database():
    from lightmdb import get_db
    return get_db(current_app)


class Director(object):
    """Director Model."""
    TABLE_NAME = 'directors'

    def __init__(self, pk=None, movie_pk=None, celebrity_pk=None):
        self.pk = pk
        self.movie_pk = movie_pk
        self.celebrity_pk = celebrity_pk

    def get_id(self):
        return str(self.pk)

    def values(self):
        data = OrderedDict([
            ('pk', self.pk),
            ('movie_pk', self.movie_pk),
            ('celebrity_pk',self.celebrity_pk)
        ])
        return data

    @classmethod
    def get(cls, pk=None):
        """Get director by identifier.

        Usage: Director.get(title)
        :rtype: Director object or None
        """
        db = get_database()
        cursor = db.cursor
        if pk:
            cursor.execute(
                "SELECT * FROM {table} WHERE id=%(id)s".format(table=cls.TABLE_NAME),
                {'id': pk}
            )
        else:
            return None
        director = db.fetch_execution(cursor)
        if director:
            return Director(**director[0])
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
        directors = db.fetch_execution(cursor)
        result = []
        for director in directors:
            result.append(Director(**director))
        return result

    def delete(self):
        if not self.pk:
            raise ValueError("Director is not saved yet.")
        db = get_database()
        cursor = db.cursor
        query = "DELETE FROM {table} WHERE id=%(id)s".format(table=self.TABLE_NAME)
        cursor.execute(query, {'id': self.pk})
        db.commit()

    def save(self):
        db = get_database()
        data = self.values()
        if self.pk:
            director = self.get(pk=self.pk)
        else:
            director = self.get(title=self.title)
        if director:
            # update old director
            old_data = director.values()
            diffkeys = [key for key in data if data[key] != old_data[key]]
            if not diffkeys:
                # Nothing changed
                return director
            filters = {}
            for key in diffkeys:
                filters[key] = self.values()[key]
            query = "UPDATE {table} SET ".format(table=self.TABLE_NAME)
            for key in filters:
                query += key + ' = %(' + key + ')s, '
            # Remove last comma
            query = query.rstrip(', ') + ' '
            # Add filter
            query += "WHERE id={pk}".format(pk=director.pk)
            db.cursor.execute(query, filters)
            db.commit()
            # Return saved director role
            return self.get(pk=director.pk)
        # new director role
        del data['pk']
        query = "INSERT INTO {table} " \
                "(movie_pk, celebrity_pk) VALUES" \
                "(%(movie_pk)s, %(celebrity_pk)s)".format(table=self.TABLE_NAME)
        db.cursor.execute(query, dict(data))
        db.commit()
        return self.get(title=self.title)
