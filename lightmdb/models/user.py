from flask import current_app
from flask_login import UserMixin
from collections import OrderedDict
from werkzeug.security import generate_password_hash, check_password_hash


def get_database():
    from lightmdb import get_db
    return get_db(current_app)


class User(UserMixin):
    """User Model."""
    TABLE_NAME = 'users'
    def __init__(self, pk=None, username=None, password=None, email=None, name=None,
                 confirmed_at=None, deleted=False, is_staff=False):
        self.pk = pk
        self.username = username
        self.password = password
        self.email = email
        self.name = name
        self.confirmed_at = confirmed_at
        self.deleted = bool(deleted)
        self.is_staff = is_staff
        if not self.pk and self.password:
            # new user
            self.set_password()

    def __repr__(self):
        if self.name:
            return self.name
        return self.username

    @property
    def is_active(self):
        return not self.deleted

    def get_id(self):
        return str(self.pk)

    def set_password(self, password=None):
        """Make password hash."""
        if password:
            self.password = password
        self.password = generate_password_hash(self.password)

    def check_password(self, password):
        """Check password match with hash."""
        return check_password_hash(self.password, password)

    def values(self):
        data = OrderedDict([
            ('pk', self.pk),
            ('username', self.username),
            ('password', self.password),
            ('email', self.email),
            ('name', self.name),
            ('confirmed_at', self.confirmed_at),
            ('deleted', self.deleted),
            ('is_staff', self.is_staff)
        ])
        return data

    @classmethod
    def get(cls, pk=None, username=None, email=None):
        """Get user by identifier.

        Usage: User.get(user_id)
        :rtype: User object or None
        """
        db = get_database()
        cursor = db.cursor
        if pk:
            cursor.execute(
                "SELECT * FROM {table} WHERE id=%(id)s".format(table=cls.TABLE_NAME),
                {'id': pk}
            )
        elif username:
            cursor.execute(
                "SELECT * FROM {table} WHERE username=%(username)s".format(table=cls.TABLE_NAME),
                {'username': username}
            )
        elif email:
            cursor.execute(
                "SELECT * FROM {table} WHERE email=%(email)s".format(table=cls.TABLE_NAME),
                {'email': email}
            )
        else:
            return None
        user = db.fetch_execution(cursor)
        if user:
            return User(**user[0])
        return None

    @classmethod
    def filter(cls, **kwargs):
        db = get_database()
        cursor = db.cursor
        query = "SELECT * FROM " + cls.TABLE_NAME
        if kwargs:
            filter_query, filter_data = db.where_builder(kwargs)
            query += " WHERE " + filter_query
        cursor.execute(query, filter_data)
        users = db.fetch_execution(cursor)
        result = []
        for user in users:
            result.append(User(**user))
        return result

    def delete(self):
        if not self.pk:
            raise ValueError("User is not saved yet.")
        db = get_database()
        cursor = db.cursor
        query = "UPDATE {table} SET deleted = TRUE WHERE id=%(id)s".format(table=self.TABLE_NAME)
        cursor.execute(query, {'id': self.pk})
        db.commit()

    def save(self):
        db = get_database()
        cursor = db.cursor
        data = self.values()
        # use filter for django as it raises exception instead of None return
        user = self.get(username=self.username)
        if user:
            # update old user
            old_data = user.values()
            diffkeys = [key for key in data if data[key] != old_data[key]]
            if not diffkeys:
                # Nothing changed
                return user
            filters = {}
            for key in diffkeys:
                filters[key] = self.values()[key]
            query = "UPDATE {table} SET ".format(table=self.TABLE_NAME)
            for key in filters:
                query += key + ' = %(' + key + ')s, '
            # Remove last comma
            query = query.rstrip(', ') + ' '
            # Add filter
            query += "WHERE id={pk}".format(pk=user.pk)
            cursor.execute(query, filters)
            db.commit()
            # Return saved user
            return self.get(pk=user.pk)
        # new user
        del data['pk']
        query = "INSERT INTO {table} " \
                "(username, email, name, confirmed_at, is_staff, password) " \
                "VALUES" \
                "(%(username)s, %(email)s, %(name)s, %(confirmed_at)s, " \
                "%(is_staff)s, %(password)s)".format(table=self.TABLE_NAME)
        cursor.execute(query, dict(data))
        db.commit()
        return self.get(username=self.username)
