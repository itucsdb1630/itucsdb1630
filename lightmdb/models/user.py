"""User Models."""

class Role(object):
    """User Role for Permissions."""
    def __init__(self, name=None, description=None):
        self.name = name
        self.description = description
    
    def get(db, pk):
        db.cursor.execute("SELECT * FROM role WHERE id={pk}", {'pk':pk})
        return db.fetch_execution()

class User(object):
    """User Model."""
    def __init__(self, pk=None, username=None, email=None, password=None, name=None,
                 active=True, confirmed_at=None, roles=[], is_staff=False):
        self.pk = pk
        self.username = username
        self.email = email
        self.name = name
        self.active = active
        self.confirmed_at = confirmed_at
        self.roles = roles
        self.is_staff = is_staff
        self.password = password

    def check_data(self):
        """Check if all required data presents."""
        pass

    def set_password(self, password):
        """Make password hash."""
        self.password = password
    
    def get(self, db, pk=None, username=None):
        cursor = db.cursor
        if pk:
            cursor.execute("SELECT * FROM users WHERE id=%(pk)s", {'pk': pk})
        elif username:
            cursor.execute("SELECT * FROM users WHERE username=%(username)s", {'username': username})
        else:
            return None
        user = db.fetch_execution(cursor)
        if user:
            return User(**user[0])
        return None

    def filter(self, db, **kwargs):
        return None

    def save(self, db):
        self.check_data()
        user = self.filter(db, username=self.username)
        if user:
            # update
            # @TODO
            raise NotImplemented
            return self.get(db, username=self.username)
            # new
        data = {
            'username': self.username,
            'email': self.email,
            'name': self.name,
            'active': self.active,
            'confirmed_at': self.confirmed_at,
            'is_staff': self.is_staff,
            'password': self.password
        }
        query = "INSERT INTO users " \
                "(username, email, name, active, confirmed_at, is_staff, password) " \
                "VALUES" \
                "(%(username)s, %(email)s, %(name)s, %(active)s, %(confirmed_at)s, " \
                "%(is_staff)s, %(password)s)"

        print(query)
        db.cursor.execute(query, data)
        db.commit()
        return self.get(db, username=self.username)
        