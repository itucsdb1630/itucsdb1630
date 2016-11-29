from flask import current_app


def get_database():
    from lightmdb import get_db
    return get_db(current_app)

class ContactComment(object):

    TABLE_NAME = 'contactComments'

    new_comment=None
    pk=None

    def __init__(self,pk_contact=None,comment=None,send_mail=None,pk=None):
        if pk_contact:
            self.pk_contact=str(pk_contact)
        if pk:
            self.pk = str(pk)
        if comment:
            self.comment=str(comment)
            self.new_comment=True
        self.send_mail=send_mail



    def get_comments_by_contact_id(self):
        try:
            db = get_database()
            cursor = db.cursor
            cursor.execute("SELECT id,comment,sendmail,sendtime FROM {table} WHERE pk_contact=%s".format(table=self.TABLE_NAME),[self.pk_contact])
            contact_info= cursor.fetchall()
            if contact_info:
                return contact_info
        except:
            return False

    def delete_comments_by_contact_id(self):
        try:
            db = get_database()
            cursor = db.cursor
            cursor.execute("DELETE FROM {table} WHERE pk_contact=%s".format(table=self.TABLE_NAME),[self.pk_contact])
            contact_info= cursor.fetchall()
            if contact_info:
                return contact_info
        except:
            return False

    def delete_comments_by_id(self):
        try:
            db = get_database()
            cursor = db.cursor
            cursor.execute("DELETE FROM {table} WHERE pk_contact=%s".format(table=self.TABLE_NAME),[self.pk])
            contact_info= cursor.fetchall()
            if contact_info:
                return contact_info
        except:
            return False

    def update_comment(self,comment,sendmail):
        try:
            db = get_database()
            cursor = db.cursor
            cursor.execute("UPDATE {table} set comment=%s , sendmail=%s WHERE id=%s".format(table=self.TABLE_NAME),[comment,sendmail,self.pk])
            contact_info= cursor.fetchall()
            if contact_info:
                return contact_info
        except:
            return False

    def save(self):
        try:
            db = get_database()
            db.cursor.execute("INSERT INTO {table} (pk_contact,comment,sendmail) VALUES (%s,%s,%s)".format(table=self.TABLE_NAME),[self.pk_contact,self.comment,self.send_mail])
            db.commit()
            return True
        except:
            return False
