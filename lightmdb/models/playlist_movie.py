from flask import current_app
from lightmdb.models import Movie

def get_database():
    from lightmdb import get_db
    return get_db(current_app)

class Playlist_Movie():
    """Playlist_Movie Model."""
    TABLE_NAME = 'playlist_movies'

    def __init__(self,pk=None,playlist_id=None,movie_id=None,ordering=None):
        self.pk = pk
        self.playlist_id = playlist_id
        self.movie_id = movie_id
        self.ordering = ordering

    @classmethod
    def get(cls, pk=None):
        db = get_database()
        cursor = db.cursor
        if pk:
            cursor.execute(
                "SELECT * FROM {table} WHERE id=%(id)s".format(table=cls.TABLE_NAME), {'id':pk}
    )
        else:
            return None
        playlist_movie = db.fetch_execution(cursor)
        if playlist_movie:
            return Playlist_Movie(**playlist_movie[0])
        return None

    @classmethod
    def get_by_playlist(cls, playlist_id=None):
        db = get_database()
        cursor = db.cursor
        if playlist_id:
            cursor.execute(
                "SELECT * FROM {table} WHERE playlist_id=%(playlist_id)s".format(table=cls.TABLE_NAME), {'playlist_id':playlist_id}
    )
        else:
            return None
        playlist_movies = db.fetch_execution(cursor)
        if playlist_movies:
            pl_movies = []
            for item in playlist_movies:
                pl_movies.append[Playlist_Movie(**item)]
            movie_entries = []
            for item in pl_movies:
                _movie = Movie.get(item.movie_id)
                if _movie:
                    movie_entries.append(_movie)
            return movie_entries
        return None


    def delete(self):
        if not self.pk:
            raise ValueError("Playlist Movie isn't saved yet.")
        db = get_database()
        cursor = db.cursor
        query = "DELETE FROM {table} WHERE id=%(id)s".format(table=self.TABLE_NAME)
        cursor.execute(query, {'id':self.pk})
        db.commit()



    def save(self):
        db = get_database()
        data = self.values()
        if self.pk:
            playlist_movie = self.get(pk=self.pk)
        else:   
            playlist_movie = self.get(title=self.title)
        if playlist_movie:
            # update old playlist_movie
            old_data = playlist_movie.values()
            diffkeys = [key for key in data if data[key] != old_data[key]]
            if not diffkeys:
                # Nothing changed
                return playlist_movie
            filters = {}
            for key in diffkeys:
                filters[key] = self.values()[key]
            query = "UPDATE {table} SET ".format(table=self.TABLE_NAME)
            for key in filters:
                query += key + ' = %(' + key + ')s, '
            # Remove last comma
            query = query.rstrip(', ') + ' '
            # Add filter
            query += "WHERE id={pk}".format(pk=playlist_movie.pk)
            db.cursor.execute(query, filters)
            db.commit()
            # Return saved playlist_movie
            return self.get(pk=playlist_movie.pk)
        # new playlist_movie
        del data['pk']
        query = "INSERT INTO {table} " \
                "(playlist_id,movie_id,ordering) " \
                "VALUES" \
                "(%(playlist_id)s, %(movie_id)s, %(ordering)s,)".format(table=self.TABLE_NAME)
        db.cursor.execute(query, dict(data))
        db.commit()
        return self.get(pk=self.pk)

