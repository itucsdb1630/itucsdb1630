from flask import current_app


def get_database():
    from lightmdb import get_db
    return get_db(current_app)

class MovieTags:

    def __init__(self,movie_tag_id=None,movie_id=None,tag_id=None):
        self.mt_id=movie_tag_id
        self.movie_id=movie_id
        self.tag_id =tag_id
        if self.mt_id:
            movie_tag = self.get_movie_tag_by_id()
            if movie_tag and len(movie_tag)!=0:
                self.movie_id=movie_tag[0]
                self.tag_id=movie_tag[2]

    def get_movie_tag_by_id(self):
        try:
            db = get_database()
            cursor = db.cursor
            cursor.execute("SELECT movies.id,movies.title,tags.id,tags.name From movietags join tags on movietags.tagid = tags.id JOIN movies on movietags.movieid = movies.id WHERE id=%s",[self.mt_id])
            tag= cursor.fetchone()
            if tag:
                return tag
        except:
            return False

    def get_movie_tags_by_tag_id(self):
        try:
            db = get_database()
            cursor = db.cursor
            cursor.execute("SELECT tags.id,tags.name FROM movietags JOIN tags on movietags.tagid = tags.id WHERE movieid=%s",[self.movie_id])
            movie_tags= cursor.fetchall()
            if movie_tags:
                return movie_tags
        except:
            return False

    def get_tag_movies_by_movie_id(self):
        try:
            db = get_database()
            cursor = db.cursor
            cursor.execute("SELECT * FROM movietags JOIN  movies on movietags.movieid = movies.id WHERE tagid=%s",[self.tag_id])
            tag_movies= cursor.fetchall()
            if tag_movies:
                return tag_movies
        except:
            return False

    def control_tag_movie_by_movie_id_and_tag_id(self):
        try:
            db = get_database()
            cursor = db.cursor
            cursor.execute("SELECT * FROM movietags WHERE tagid=%s and movieid=%s",[self.tag_id,self.movie_id])
            tag_movies= cursor.fetchone()
            if tag_movies:
                return True
            else:
                return False
        except:
            return False

    def save(self):
        if self.movie_id and self.tag_id and not self.control_tag_movie_by_movie_id_and_tag_id():
            try:
                db = get_database()
                cursor = db.cursor
                cursor.execute("INSERT into movietags (movieid,tagid) VALUES (%s,%s)", [self.movie_id,self.tag_id])
            except:
                return False

    def update_name(self,tag_id,movie_id):
        try:
            db = get_database()
            cursor = db.cursor
            cursor.execute("UPDATE movietags SET movieid=%s , tagid=%s WHERE id=%s", [movie_id,tag_id,self.tag_id])
        except:
            return False
