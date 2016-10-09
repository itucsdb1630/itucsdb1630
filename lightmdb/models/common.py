"""Common Classes for App."""
from flask_security.datastore import Datastore, UserDatastore


class PostgresDatastore(Datastore):
    """Custom Datastore for Postgres."""
    def commit(self):
        self.db.commit()

    def put(self, model):
        model.save(self.db)

    def delete(self, model):
        model.delete(self.db)


class PostgresUserDatastore(PostgresDatastore, UserDatastore):
    """Custom Datastore for users."""
    def __init__(self, db, user_model, role_model):
        self.db = db
        PostgresDatastore.__init__(self, db)
        UserDatastore.__init__(self, user_model, role_model)

    def _is_numeric(self, value):
        try:
            int(value)
        except (TypeError, ValueError):
            return False
        return True

    def get_user(self, identifier):
        if self._is_numeric(identifier):
            return self.user_model.get(self.db, identifier)
        for attr in get_identity_attributes():
            rv = self.user_model.filter(self.db, attr=identifier, limit=1)
            if rv:
                return rv
        return None

    def find_user(self, **kwargs):
        return self.user_model.filter(self.db, **kwargs, limit=1)

    def find_role(self, role):
        return self.role_model.filter(self.db, name=role, limit=1)


class Database(object):
    def __init__(self, connection=None):
        self.connection = connection

    @property
    def cursor(self):
        return self.connection.cursor()

    def set(self, connection=None):
        self.connection = connection
        if self.connection:
            self.cursor = connection.cursor()

    def commit(self):
        self.connection.commit()

    def execute(self, *args, **kwargs):
        self.cursor.execute(*args, **kwargs)

    @staticmethod
    def fetch_execution(cursor):
        """Get results as dictionary.

        After cursor.execute command call this method to get `fetchall`
        results as dictionary list with column names.
        """
        results = []
        items = cursor.fetchall()
        columns = [i[0] for i in cursor.description]
        for item in items:
            data = {}
            for i in range(len(columns)):
                if columns[i] == 'id':
                    data['pk'] = item[i]
                else:
                    data[columns[i]] = item[i]
            results.append(data)
        return results

    def close(self):
        if self.connection:
            self.connection.close()
