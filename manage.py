#!/usr/bin/env python3
import os
from flask_script import Manager, Server, Shell, Command, Option

from lightmdb import create_app, get_db, close_db, init_db
from lightmdb.models import User
# Get local settings
try:
    import local_settings as settings
except ImportError as e:
    if "local_settings" not in str(e):
        raise e
    settings = None

manager = Manager(create_app)
app = create_app()


@app.teardown_appcontext
def close_context(error=None):
    close_db()

HOST = None
PORT = None
VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
if VCAP_APP_PORT:
    HOST = "0.0.0.0"
    PORT = VCAP_APP_PORT
elif os.getenv('CI_TESTS'):
    HOST = "0.0.0.0"
    PORT = 5000
else:
    HOST = getattr(settings, "HOST", "127.0.0.1")
    PORT = getattr(settings, "PORT", 5000)


class Migration(Command):
    """Initialize Database."""
    def run(self):
        with app.app_context():
            init_db(app)


class CreateUser(Command):
    """Create new user."""
    option_list = (
        Option('--username', '-u', dest='username', required=True),
        Option('--password', '-p', dest='password', required=True),
        Option('--email', '-e', dest='email', required=True),
        Option('--staff', '-s', dest='is_staff'),
    )

    def run(self, username, password, email, is_staff=False):
        user = User(username=username, password=password, email=email, is_staff=is_staff)
        user = user.save()
        print("User %s created with id %d" % (user.username, user.pk))

def _make_context():
    with app.app_context():
        return dict(app=app, db=get_db(app))

manager.add_command('shell', Shell(make_context=_make_context, use_ipython=True))
manager.add_command('migrate', Migration())
manager.add_command('createuser', CreateUser())
manager.add_command('runserver', Server(host=HOST, port=PORT, threaded=True))

if __name__ == '__main__':
    manager.run()
