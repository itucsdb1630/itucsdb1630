from flask import current_app


def get_database():
    from lightmdb import get_db
    return get_db(current_app)


class ContactMessage(object):

    TABLE_NAME = 'contactUs'
    def __init__(self,cid=None,title=None,content=None,email=None,phone=None):
        if cid:
            self.cid = int(cid)
        if title:
            self.title=str(title)
        if content:
            self.content=str(content)
        if email:
            self.email=str(email)
        if phone:
            self.phone=str(phone)
        if cid:
            self.saved_message=True
            contact_info=self.get_info_by_id()
            if contact_info:
                self.title = contact_info[0]
                self.content = contact_info[1]
                self.email = contact_info[2]
                self.phone = contact_info[3]
                self.status =contact_info[4]
                self.sendTime = contact_info[5]
        else:
            self.saved_message=False

    def validate_info(self):
        if 0 < len(self.title) < 100 and 0 < len(self.content) < 255 and 0 < len(self.email) < 50 and 0 < len(
            self.phone) < 50:
            return True
        return False

    def get_info_by_id(self):
        try:
            db = get_database()
            cursor = db.cursor
            cursor.execute("SELECT title,content,email,phone,status,sendtime FROM {table} WHERE id=%s".format(table=self.TABLE_NAME),[self.cid])
            contact_info= cursor.fetchone()
            if contact_info:
                return contact_info
        except:
            return False

    def change_status(self,new_status):
        all_status=['new','replied','waiting','spam','closed']
        if new_status in all_status:
            self.status = new_status
            try:
                db = get_database()
                cursor = db.cursor
                cursor.execute("UPDATE {table} SET status=%s WHERE id=%s".format(table=self.TABLE_NAME), [new_status,self.cid])
                db.commit()
                return True
            except:
                return False
        return False

    def delete_message(self):
        db = get_database()
        ##cursor.execute("UPDATE {table} SET deleted=1 WHERE id=%".format(table=self.TABLE_NAME), [self.cid])
        db.cursor.execute("DELETE FROM {table} WHERE id=%s".format(table=self.TABLE_NAME), [self.cid])
        db.commit()

    def save(self):
        try:
            db = get_database()
            db.cursor.execute("INSERT INTO {table} (title,content,email,phone) VALUES (%s,%s,%s,%s)".format(table=self.TABLE_NAME),[self.title,self.content,self.email,self.phone])
            db.commit()
            return True
        except:
            return False

    @staticmethod
    def get_messages(desired_status=None,get_deleted=False):
        db = get_database()
        cursor = db.cursor
        accepted_status=[]
        all_status = ['new', 'replied', 'waiting', 'spam', 'closed']
        if not desired_status:
            desired_status = ['new','replied','waiting']
        for one_status in desired_status:
            if one_status in all_status:
                accepted_status.append(one_status)
        where =''
        if not get_deleted:
            where = 'deleted=False and (status=\''
        if len(accepted_status) > 0:
            where += '\' or status =  \''.join(accepted_status)
            where += '\')'
            cursor.execute("SELECT id,title,content,email,phone,status,sendtime from contactUs where  "+where)
            result = cursor.fetchall()
            if result:
                return result
            return []
        return []
