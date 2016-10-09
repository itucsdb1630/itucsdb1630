import os
from flask import current_app
from flask_script import Manager, Server, Shell

from lightmdb import create_app, get_db
# Get local settings
try:
    import local_settings as settings
except ImportError as e:
    if "local_settings" not in str(e):
        raise e
    settings = None

manager = Manager(create_app)
app = create_app()

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


def _make_context():
    with app.app_context():
        return dict(app=app, db=get_db(app))

manager.add_command("shell", Shell(make_context=_make_context))
manager.add_command('runserver', Server(host=HOST, port=PORT))

if __name__ == '__main__':
    manager.run()
