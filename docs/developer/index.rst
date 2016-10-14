Developer Guide
===============

INSTALL
-------
Project uses postgres as database. You need to install postgresql locally or use vagrant.

By default application uses vagrant settings for database. If you installed it locally you will need to set DSN in `local_settings`.

**Prepare Environment**:

* Create virtual environment in venv folder:
    `$ virtualenv venv -p python3`
* Install project requirements:
    `$ pip install -r requirements.py`
* Initialize database:
    `$ python manage.py migrate`
* Run application:
    `$ python manage.py runserver`

**local_settings File**::

* Create "local_settings.py" file in project root directory.
* Add custom settings to file.

**Available Settings**::

>>> DEBUG=True        # Debug mode
>>> DSN="..."         # Postgres credentials, check `DEFAULT_DSN` in `application.py` file.
>>> HOST="127.0.0.1"  # Application host
>>> PORT=5000         # Application port
>>> SENTRY_DSN="..."  # Sentry dsn setting

**Environment Variables**::

* 'VCAP_APP_PORT' - Bluemix application port
* 'VCAP_SERVICES' - Bluemix settings for services
* 'SENTRY_DSN' - Sentry DSN (logging)
* 'CI_TESTS' - Travis CI environment
* 'SECRET_KEY' - Secret key for cookies

Database Design
---------------

**explain the database design of your project**

**include the E/R diagram(s)**

Code
----

**Creating new models**:

Create your new models inside lightmdb/models/ folder.

As everyone in team should write few sql command, we will not use Base objects.

Each object should have `get`, `filter`, `save` and `delete` methods::

   .. code-block:: python

      class Movie:
         @staticmethod
         def get(pk=None):
            # Fetch movie from database as dictionary
            # Return Movie object with database values
            # If there is no matching result, return None

         @staticmethod
         def filter(**kwargs):
            # Fetch movie using parameters (filters) in kwargs
            # return list of Movie objects
            # If there is no matching result, return empty list ([])

         def save(self):
            # if self.pk is present, update database with current values
            # if it is new object, insert into database
            # Return call to get method:
            return Movie.get(identifier=self.identifier)

         def delete(self):
            # If object is not populated from database, ie. self.pk is None:
            raise ValueError("Movie is not saved yet.")
            # Delete Movie using identifier from database.
            # Do not return anything

After creating model add it to lightmdb/models/__init__.py file.

**Create Form for each Model**:

In order to safely create Model using user's request parameters create Form based on Model.

Forms should be under lightmdb/forms/ folder.

After creating form add it to lightmdb/forms/__init__.py file.

**Creating View**:

* NotImplemented

**Add view to urls**:

* NotImplemented

Work done by each team member:
------------------------------
List with issues for each team member can be found on `Github Projects <https://github.com/itucsdb1630/itucsdb1630/projects/1>`_

.. toctree::

   member1
   member2
   member3
   member4
   member5
