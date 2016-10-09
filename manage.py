import os
from flask import current_app
from flask_script import Manager, Server

from lightmdb import create_app
# Get local settings
try:
    import local_settings as settings
except ImportError as e:
    if "local_settings" not in str(e):
        raise e
    settings = None

manager = Manager(create_app)
app = create_app

VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
if VCAP_APP_PORT:
    manager.add_command('runserver', Server(
        host="0.0.0.0",
        port=VCAP_APP_PORT
    ))
elif os.getenv('CI_TESTS'):
    manager.add_command('runserver', Server(
        host="127.0.0.1",
        port=5000
    ))
else:
    manager.add_command('runserver', Server(
        host=getattr(settings, "HOST", "127.0.0.1"),
        port=getattr(settings, "PORT", 5000)
    ))

if __name__ == '__main__':
    manager.run()
