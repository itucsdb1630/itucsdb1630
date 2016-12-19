from flask import current_app
from collections import OrderedDict
from datetime import datetime


def get_database():
    from lightmdb import get_db
    return get_db(current_app)


class StatusMessage(object):
    """Status Message Model."""
    TABLE_NAME = 'status_messages'

    def __init__(self, pk=None, user_id=None, movie_id=None, message=None, added_at=datetime.now()):
        self.pk = pk
        self.user_id = user_id
        self.movie_id = movie_id
        self.message = message
        self.added_at = added_at

    @property
    def user(self):
        from lightmdb.models import User
        return User.get(pk=self.user_id)

    @property
    def movie(self):
        from lightmdb.models import Movie
        return Movie.get(pk=self.movie_id)

    def get_id(self):
        return str(self.pk)

    def values(self):
        data = OrderedDict([
            ('pk', self.pk),
            ('user_id', self.user_id),
            ('movie_id', self.movie_id),
            ('message', self.message),
            ('added_at', self.added_at),
        ])
        return data

    @classmethod
    def get(cls, pk=None):
        """Get message by identifier.

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
        else:
            return None
        message = db.fetch_execution(cursor)
        if message:
            return StatusMessage(**message[0])
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
        messages = db.fetch_execution(cursor)
        result = []
        for message in messages:
            result.append(StatusMessage(**message))
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
        message = None
        if self.pk:
            message = self.get(pk=self.pk)
        if message:
            # update old message
            old_data = message.values()
            diffkeys = [key for key in data if data[key] != old_data[key]]
            if not diffkeys:
                # Nothing changed
                return message
            filters = {}
            for key in diffkeys:
                filters[key] = self.values()[key]
            query = "UPDATE {table} SET ".format(table=self.TABLE_NAME)
            for key in filters:
                query += key + ' = %(' + key + ')s, '
            # Remove last comma
            query = query.rstrip(', ') + ' '
            # Add filter
            query += "WHERE id={pk}".format(pk=message.pk)
            db.cursor.execute(query, filters)
            db.commit()
            # Return saved message
            return self.get(pk=message.pk)
        # new movie
        del data['pk']
        data['added_at'] = datetime.now()
        query = "INSERT INTO {table} " \
                "(user_id, movie_id, message, added_at) VALUES (%(user_id)s, %(movie_id)s, %(message)s, " \
                " %(added_at)s)".format(table=self.TABLE_NAME)
        if return_obj:
            query += " RETURNING id"
        cursor = db.cursor
        cursor.execute(query, dict(data))
        if return_obj:
            new_row_pk = cursor.fetchone()[0]
            return self.get(pk=new_row_pk)
        # db.commit()
        return True
