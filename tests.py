import os
from lightmdb import create_app, get_db
import unittest

class LightmdbTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.db = None
        # self.tests = db.cursor.execute()

    def tearDown(self):
        if self.db:
            self.db.close()
    
    def test_database(self):
        with self.app.app_context():
            self.db = get_db(self.app)

if __name__ == '__main__':
    unittest.main()
