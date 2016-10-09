"""Common Classes for App."""


class Database(object):
    def __init__(self, connection=None):
        self.connection = connection
        if self.connection:
            self.cursor = connection.cursor()

    def set(self, connection=None):
        self.connection = connection
        if self.connection:
            self.cursor = connection.cursor()

    def commit(self):
        self.connection.commit()

    def execute(self, *args, **kwargs):
        self.cursor.execute(*args, **kwargs)

    def close(self):
        if self.connection:
            self.connection.close()
