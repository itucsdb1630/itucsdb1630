"""Common Classes for App."""


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
