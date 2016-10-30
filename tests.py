from lightmdb import create_app, get_db, init_db
from lightmdb.models import User
import unittest


class LightmdbTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.db = None
        with self.app.app_context():
            init_db(self.app)

    def tearDown(self):
        if self.db:
            self.db.close()

    def test_database(self):
        with self.app.app_context():
            self.db = get_db(self.app)

    def test_user(self):
        with self.app.app_context():
            admin = User.get(username='admin')
            self.assertTrue(admin is not None)
            admin.set_password('admin')
            user = User(username='test', name='Test User', password='test', email="info+test@lightmdb.org")
            self.assertFalse(user.password == 'test')
            self.assertTrue(user.check_password('test'))
            self.assertTrue(user.is_active)
            self.assertTrue(user.pk is None)
            # get user from db
            new_user = User.get(username='test')
            self.assertFalse(new_user is not None)
            user.save()
            new_user = User.get(username='test')
            self.assertTrue(new_user is not None)
            self.assertEqual(new_user.email, user.email)
            self.assertTrue(new_user.pk is not None)
            # Test Update
            self.assertEqual(new_user.name, 'Test User')
            new_user.name = 'Awesome User'
            user = new_user.save()
            self.assertEqual(user.name, 'Awesome User')

if __name__ == '__main__':
    unittest.main()
