from flask import current_app


def get_database():
    from lightmdb import get_db
    return get_db(current_app)

class Tag:

    def __init__(self,tag_id=None,tag_name=None):
        self.tag_id=tag_id
        self.name=tag_name
        if tag_id:
            tag = self.get_tag_by_id()
            if tag and len(tag)!=0:
                self.name=tag[1]

    def get_tag_by_id(self):
        try:
            db = get_database()
            cursor = db.cursor
            cursor.execute("SELECT id,name From tags WHERE id=%s",[self.tag_id])
            tag= cursor.fetchone()
            if tag:
                return tag
        except:
            return False

    def get_tag_by_name(self):
        try:
            db = get_database()
            cursor = db.cursor
            cursor.execute("SELECT id,name From tags WHERE name=%s",[self.name])
            tag= cursor.fetchone()
            if tag:
                return tag
        except:
            return False
    @staticmethod
    def get_tags():
        try:
            db = get_database()
            cursor = db.cursor
            cursor.execute("SELECT id,name From tags ")
            tag= cursor.fetchall()
            return tag
        except:
            return False

    def save(self):
        if len(self.name)!=0 and not self.get_tag_by_name():
            try:
                db = get_database()
                cursor = db.cursor
                cursor.execute("INSERT into tags (name) VALUES (%s)", [self.name])
            except:
                return False

    def delete(self):
        try:
            db = get_database()
            cursor = db.cursor
            cursor.execute("DELETE FROM tags WHERE id=%s", [self.tag_id])
        except:
            return False

    def update_name(self,name):
        try:
            db = get_database()
            cursor = db.cursor
            cursor.execute("UPDATE tags SET name=%s WHERE id=%s", [name,self.tag_id])
        except:
            return False
