from flask import Flask, g
from flask_login import LoginManager
from flask_wtf.csrf import CsrfProtect
from raven.contrib.flask import Sentry
from flask_gravatar import Gravatar
import psycopg2 as dbapi2
import os
import json
import re

from lightmdb import views
from lightmdb import models

# Get local settings
try:
    import local_settings as settings
except ImportError as e:
    if "local_settings" not in str(e):
        raise e
    settings = None


__all__ = ['create_app', 'get_db', 'close_db', 'init_db', ]

DEFAULT_APP_NAME = 'lightmdb'
DEFAULT_APP_SECRET = 'Secret@LightMDB'
DEFAULT_DSN = "user='vagrant' password='vagrant' host='localhost' port=54321 dbname='itucsdb'"

DEFAULT_BLUEPRINTS = (
    # Add blueprints here
    (views.frontend, ""),
    (views.admin, "/admin"),
    (views.user, "/profile"),
    (views.messenger, "/messenger"),
    (views.contactus, "/contact"),
    (views.playlist, "/playlist"),
    (views.toplist, "/toplists"),
    (views.movies, "/movies"),
)

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return models.User.get(user_id)


def create_app():
    """Create application and set settings."""
    app = Flask(DEFAULT_APP_NAME)
    # Session settings
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', DEFAULT_APP_SECRET)
    app.config['SESSION_COOKIE_NAME'] = 'Ssession'
    # app.config['SESSION_COOKIE_SECURE'] = True
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config['PERMANENT_SESSION_LIFETIME'] = 2678400  # seconds
    # app.config['SENTRY_RELEASE'] = fetch_git_sha(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    app.config['SECURITY_USER_IDENTITY_ATTRIBUTES'] = ['username', 'email']
    # Get environment variables
    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    # Set configuration
    if VCAP_SERVICES:
        _configure_prod(app, VCAP_SERVICES)
    elif os.getenv('CI_TESTS'):
        _configure_test(app)
    else:
        _configure_local(app)
    # Login Manager
    login_manager.init_app(app)
    login_manager.login_view = "frontend.login"
    # Protection
    CsrfProtect(app)
    # Gravatar
    app.config['gravatar'] = Gravatar(
        app, size=160, rating='g', default='retro',
        force_default=False, force_lower=False, use_ssl=True, base_url=None
    )

    # Set sentry for debugging
    if os.getenv('SENTRY_DSN'):
        sentry = Sentry(app, dsn=os.getenv('SENTRY_DSN'))
        sentry.init_app(app)
    elif getattr(settings, 'SENTRY_DSN', None):
        sentry = Sentry(app, dsn=getattr(settings, 'SENTRY_DSN', None))
        sentry.init_app(app)
    # Set views
    for view, url_prefix in DEFAULT_BLUEPRINTS:
        app.register_blueprint(view, url_prefix=url_prefix)
    return app


def init_db(app):
    """Initializes the database."""
    db = get_db(app)
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor.execute(f.read())
    db.commit()


def get_db(app):
    if not hasattr(g, 'database'):
        g.database = _connect_db(app)
    return g.database


def close_db():
    if hasattr(g, 'database'):
        g.database.close()
        del g.database


def _connect_db(app):
    return models.Database(dbapi2.connect(app.config['dsn']))


def _get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = "user='{}' password='{}' host='{}' port={} dbname='{}'".format(
        user, password, host, port, dbname
    )
    return dsn


def _configure_prod(app, configuration):
    """Production Configurations."""
    app.config['DEBUG'] = False
    app.config['dsn'] = _get_elephantsql_dsn(configuration)


def _configure_test(app):
    """Test Configurations."""
    app.config['DEBUG'] = False
    app.config['dsn'] = "user='{}' password='{}' host='{}' port={} dbname='{}'".format(
        "postgres", "", "127.0.0.1", 5432, "lightmdb_test"
    )


def _configure_local(app):
    """Local Configurations."""
    app.config['DEBUG'] = getattr(settings, 'DEBUG', True)
    app.config['dsn'] = getattr(settings, 'DSN', DEFAULT_DSN)
