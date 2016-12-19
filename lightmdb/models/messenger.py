from flask import current_app
from collections import OrderedDict


def get_database():
    from lightmdb import get_db
    return get_db(current_app)


class Messenger:
    TABLE_NAME = 'user_messages'

    def __init__(self, pk=None, sender_pk=None, receiver_pk=None, time_stamp=None, message=None):
        self.pk = pk
        self.sender_pk = sender_pk
        self.receiver_pk = receiver_pk
        self.time_stamp = time_stamp
        self.message = message

    def values(self):
        data = OrderedDict([
            ('pk', self.pk),
            ('sender_pk', self.sender_pk),
            ('receiver_pk', self.receiver_pk),
            ('time_stamp', self.time_stamp),
            ('message', self.message)
        ])
        return data

    @classmethod
    def get(cls, sender_pk=None, receiver_pk=None, time_stamp=None, pk=None):
        db = get_database()
        cursor = db.cursor
        if sender_pk and receiver_pk and time_stamp:
            cursor.execute(
                "SELECT * FROM {table} WHERE sender_pk=%(sender_pk)s AND receiver_pk=%(receiver_pk)s AND time_stamp>%(time_stamp)s".format(
                    table=cls.TABLE_NAME),
                {'sender_pk': sender_pk, 'receiver_pk': receiver_pk, 'time_stamp': time_stamp}
            )
        elif sender_pk and receiver_pk:
            cursor.execute(
                "SELECT * FROM {table} WHERE sender_pk=%(sender_pk)s AND receiver_pk=%(receiver_pk)s".format(
                    table=cls.TABLE_NAME),
                {'sender_pk': sender_pk, 'receiver_pk': receiver_pk}
            )
        elif pk:
            cursor.execute("SELECT * FROM {table} WHERE id=%(pk)s".format(table=cls.TABLE_NAME), {'pk': pk})
            message = db.fetch_execution(cursor)
            return Messenger(**message[0])
        else:
            return None

        messages = db.fetch_execution(cursor)

        if sender_pk and receiver_pk and time_stamp:
            cursor.execute(
                "SELECT * FROM {table} WHERE sender_pk=%(receiver_pk)s AND receiver_pk=%(sender_pk)s AND time_stamp>%(time_stamp)s".format(
                    table=cls.TABLE_NAME),
                {'sender_pk': sender_pk, 'receiver_pk': receiver_pk, 'time_stamp': time_stamp}
            )
        elif sender_pk and receiver_pk:
            cursor.execute(
                "SELECT * FROM {table} WHERE sender_pk=%(receiver_pk)s AND receiver_pk=%(sender_pk)s".format(
                    table=cls.TABLE_NAME),
                {'sender_pk': sender_pk, 'receiver_pk': receiver_pk}
            )
        else:
            return None

        def get_key(custom):
            return custom['time_stamp']

        messages += db.fetch_execution(cursor)
        messages = sorted(messages, key=get_key)
        if messages:
            return messages
        return []

    def save(self):
        db = get_database()
        data = self.values()
        message = None
        if self.pk:
            message = self.get(pk=self.pk)
        if message:
            query = "UPDATE {table} SET message = %(message)s WHERE id = %(pk)s".format(table=self.TABLE_NAME)
            db.cursor.execute(query, {'pk': message.pk, 'message': self.message})
            return self.get(pk=self.pk)
        del data['pk']
        del data['time_stamp']
        query = "INSERT INTO {table} " \
                "(sender_pk, receiver_pk, message) " \
                "VALUES" \
                "(%(sender_pk)s, %(receiver_pk)s, %(message)s)".format(table=self.TABLE_NAME)
        db.cursor.execute(query, dict(data))
        return self.get(pk=self.pk)

    @classmethod
    def __delete__(cls, pk=None):
        db = get_database()
        cursor = db.cursor
        if pk:
            cursor.execute(
                "DELETE FROM {table} WHERE id=%(pk)s".format(
                    table=cls.TABLE_NAME),
                {'pk': pk}
            )
