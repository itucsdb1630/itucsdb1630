import datetime
import os
import json
import re

from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def home_page():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())


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


if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True

    VCAP_SERVICES = os.getenv('VCAP_Services')
    dsn = None
    if VCAP_SERVICES is not None:
        dsn = get_elephantsql_dsn(VCAP_SERVICES)
    else:
        try:
            with open('credentials.json', 'r') as f:
                parsed = json.load(f)
                dsn = "user='{}' password='{}' host='{}' port={} dbname='{}'".format(
                    parsed['user'], parsed['password'], parsed['host'], parsed['port'], parsed['dbname']
                )
        except FileNotFoundError:
            dsn = "user='vagrant' password='vagrant' host='localhost' port=54321 dbname='itucsdb'"
    app.config['dsn'] = dsn

    app.run(host='127.0.0.1', port=port, debug=debug)
