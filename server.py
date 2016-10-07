import datetime
import os
import json
import re

from flask import Flask
from flask import render_template

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def home_page():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())


# @emreeroglu
# for connecting project to elephant sql
# taken from https://gist.github.com/uyar/f1d6990e1807cdc1dae6
def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn


# @emreeroglu
# for reading credentials in development environment
# example json:
# {
#   "credentials": {
#     "user": "test",
#     "password": "test",
#     "host": "localhost",
#     "port": "5432",
#     "dbname": "databaseName"
#   }
# }
#
# put this json in credentials.json file

def get_credentials(LOCAL_CREDENTIALS_PATH):
    f = open(LOCAL_CREDENTIALS_PATH, 'r')
    file = f.read()
    parsedFile = json.loads(file)
    dsn = """user='{}' password='{}' host='{}' port={} dbname='{}'""".format(parsedFile['credentials']['user'],
                                                                             parsedFile['credentials']['password'],
                                                                             parsedFile['credentials']['host'],
                                                                             parsedFile['credentials']['port'],
                                                                             parsedFile['credentials']['dbname'])
    return dsn


if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True

    LOCAL_CREDENTIALS_PATH = APP_ROOT +'\\'+'credentials.json'

    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    elif os.path.isfile(LOCAL_CREDENTIALS_PATH):
        app.config['dsn'] = get_credentials(LOCAL_CREDENTIALS_PATH)
    else:
        app.config['dsn'] = """user='vagrant' password='vagrant' host='localhost' port=54321 dbname='itucsdb'"""

    app.run(host='127.0.0.1', port=port, debug=debug)
