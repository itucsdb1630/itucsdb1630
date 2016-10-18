from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


def get_database():
    from lightmdb import get_db
    return get_db(current_app)


class User(UserMixin):
    """User Model."""
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

    def __str__(self):
        return self.__repr__()

    @property
    def is_active(self):
        return self.deleted

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

    @staticmethod
    def get(pk=None, username=None, email=None):
        """Get user by identifier.

        Usage: User.get(user_id)
        :rtype: User object or None
        """
        db = get_database()
        cursor = db.cursor
        if pk:
            cursor.execute("SELECT * FROM users WHERE id=%(id)s", {'id': pk})
        elif username:
            cursor.execute("SELECT * FROM users WHERE username=%(username)s", {'username': username})
        elif email:
            cursor.execute("SELECT * FROM users WHERE email=%(email)s", {'email': email})
        else:
            return None
        user = db.fetch_execution(cursor)
        if user:
            return User(**user[0])
        return None

    @staticmethod
    def filter(**kwargs):
        db = get_database()
        cursor = db.cursor
        query = "SELECT * FROM users"
        if kwargs:
            pass
        return []

    def delete(self):
        if not self.pk:
            raise ValueError("User is not saved yet.")
        db = get_database()
        cursor = db.cursor
        query = "UPDATE users SET deleted = TRUE WHERE id=%(id)s"
        cursor.execute(query, {'id': self.pk})
        db.commit()

    def save(self):
        db = get_database()
        user = self.filter(username=self.username)
        if user:
            # update
            # @TODO
            raise NotImplemented
            return self.get(username=self.username)
            # new
        data = {
            'username': self.username,
            'email': self.email,
            'name': self.name,
            'confirmed_at': self.confirmed_at,
            'is_staff': self.is_staff,
            'password': self.password
        }
        query = "INSERT INTO users " \
                "(username, email, name, confirmed_at, is_staff, password) " \
                "VALUES" \
                "(%(username)s, %(email)s, %(name)s, %(confirmed_at)s, " \
                "%(is_staff)s, %(password)s)"

        db.cursor.execute(query, data)
        db.commit()
        return self.get(username=self.username)
