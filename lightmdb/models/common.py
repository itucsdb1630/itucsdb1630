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

    def close(self):
        if self.connection:
            self.connection.close()
