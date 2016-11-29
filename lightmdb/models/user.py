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

    @property
    def following(self):
        """Number of following users.

        :rtype: int
        """
        db = get_database()
        cursor = db.cursor
        cursor.execute("SELECT COUNT(id) FROM {table} WHERE follower_id = %(pk)s".format(
            table=Follower.TABLE_NAME),
            {'pk': self.pk}
        )
        result = cursor.fetchone()
        if result:
            return result[0]
        return 0

    @property
    def followers(self):
        """Number of followers.

        :rtype: int
        """
        db = get_database()
        cursor = db.cursor
        cursor.execute("SELECT COUNT(id) FROM {table} WHERE following_id = %(pk)s".format(
            table=Follower.TABLE_NAME),
            {'pk': self.pk}
        )
        result = cursor.fetchone()
        if result:
            return result[0]
        return 0

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
        """Get user by identifier (unique keys).

        Usage: User.get(user_id), User.get(email="emin@linux.com")
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
    def filter(cls, limit=100, order="id DESC", **kwargs):
        """Filter users.

        Usage: User.filter(is_staff=True, limit=10) -> get list of 10 staff members
        :rtype: list
        """
        query_order = None
        query_limit = None
        db = get_database()
        cursor = db.cursor
        filter_data = {}
        # Delete non-filter data
        if limit:
            query_limit = limit
            del limit
        if order:
            query_order = order
            del order
        # Select statement for query
        query = "SELECT * FROM " + cls.TABLE_NAME
        # Add filters
        if kwargs:
            filter_query, filter_data = db.where_builder(kwargs)
            query += " WHERE " + filter_query
        # Add order and limit if set
        if query_order:
            query += " ORDER BY " + query_order
        if 'ASC' not in query_order and 'DESC' not in query_order:
            query += " DESC"
        if query_limit:
            query += " LIMIT " + str(query_limit)
        # Execute query and return result
        cursor.execute(query, filter_data)
        users = db.fetch_execution(cursor)
        result = []
        for user in users:
            result.append(User(**user))
        return result

    def delete(self):
        """Delete current user.

        :NOTE: Instead of deleting it will set deleted=true in user profile
        Usage: current_user.delete()
        """
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

    # Extra function for following
    def is_following(self, pk):
        """Check if user is following someone."""
        data = Follower.get(follower_id=self.pk, following_id=pk)
        if data:
            return True
        return False

    def get_followers(self):
        """Get list of followers"""
        db = get_database()
        cursor = db.cursor
        cursor.execute("SELECT * FROM {table} WHERE following_id = %(pk)s".format(
                table=Follower.TABLE_NAME),
            {'pk': self.pk}
        )
        followers = db.fetch_execution(cursor)
        result = []
        for follower in followers:
            user = User.get(pk=follower['follower_id'])
            if user:
                result.append(user)
        return result


class Follower(object):
    """ManyToMany Following Class."""
    TABLE_NAME = 'user_followers'

    def __init__(self, pk=None, follower_id=None, following_id=None):
        self.pk = pk
        self.follower_id = follower_id
        self.following_id = following_id

    def values(self):
        data = OrderedDict([
            ('pk', self.pk),
            ('follower_id', self.follower_id),
            ('following_id', self.following_id)
        ])
        return data

    @classmethod
    def get(cls, pk=None, follower_id=None, following_id=None):
        """Get Follower data using follower and following users' id."""
        db = get_database()
        cursor = db.cursor
        if pk:
            cursor.execute(
                "SELECT * FROM {table} WHERE id = %(pk)s".format(
                    table=cls.TABLE_NAME),
                {'pk': pk}
            )
        elif follower_id and following_id:
            cursor.execute(
                "SELECT * FROM {table} WHERE follower_id = %(from)s AND following_id = %(to)s".format(
                    table=cls.TABLE_NAME),
                {'from': follower_id, 'to': following_id}
            )
        else:
            return None
        follower = db.fetch_execution(cursor)
        if follower:
            return Follower(**follower[0])
        return None

    def delete(self):
        """Unfollow.

        Usage: follow_data.delete()
        """
        if not self.pk:
            raise ValueError("Follower data is not saved yet.")
        db = get_database()
        cursor = db.cursor
        query = "DELETE FROM {table} WHERE id=%(id)s".format(table=self.TABLE_NAME)
        cursor.execute(query, {'id': self.pk})
        db.commit()

    def save(self):
        db = get_database()
        cursor = db.cursor
        data = self.values()
        # use filter for django as it raises exception instead of None return
        curr_follower = self.get(follower_id=self.follower_id, following_id=self.following_id)
        if curr_follower:
            # update old user
            old_data = curr_follower.values()
            diffkeys = [key for key in data if data[key] != old_data[key]]
            if not diffkeys:
                # Nothing changed
                return curr_follower
            filters = {}
            for key in diffkeys:
                filters[key] = self.values()[key]
            query = "UPDATE {table} SET ".format(table=self.TABLE_NAME)
            for key in filters:
                query += key + ' = %(' + key + ')s, '
            # Remove last comma
            query = query.rstrip(', ') + ' '
            # Add filter
            query += "WHERE id={pk}".format(pk=curr_follower.pk)
            cursor.execute(query, filters)
            db.commit()
            # Return saved user
            return self.get(pk=curr_follower.pk)
        # new user
        del data['pk']
        query = "INSERT INTO {table} " \
                "(follower_id, following_id) " \
                "VALUES" \
                "(%(follower_id)s, %(following_id)s)".format(table=self.TABLE_NAME)
        cursor.execute(query, dict(data))
        db.commit()
        return self.get(follower_id=self.follower_id, following_id=self.following_id)
