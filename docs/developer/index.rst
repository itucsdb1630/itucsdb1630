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
    `$ pip install -r requirements.txt`
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

* Main tables are `users` and `movies`.
* `user_followers` connects to `users` table as ManyToMany using `follower_id` and `following_id`.
* `status_messages` connects both to `movies` and `users` as ManyToOne, stores movie comments and personal status messages in timeline.
* `user_messages` connects to `users` as ManyToMany using `sender_pk` and `receiver_pk`. Stores private messages.
* `celebrities` table created for storing celebrities like actors, directors and etc.
* `casting` stores movie cast information, connects to `celebrities` using `celebrity_pk` (ManyToOne).
* `directors` acts same as casting.
* `playlists` connects to `users` as ManyToOne using `user_id`
* `playlist_movies` stores movies for playlists, connects both to `playlists` and to `movies`. Connects playlists to movies as ManyToMany.
* 

**include the E/R diagram(s)**

Code
----

**Creating new models**:

* Create your new models inside lightmdb/models/ folder.
* As everyone in team should write few sql command, we will not use Base objects.
* Each object should have `get`, `filter`, `save` and `delete` methods::

   .. code-block:: python

      class Movie:
         @classmethod
         def get(cls, pk=None):
            # Use Unique keys as possible parameters for function
            # Fetch movie from database as dictionary
            # Return Movie object with database values
            # If there is no matching result, return None

         @classmethod
         def filter(cls, limit=100, order="id DESC", **kwargs):
            # Fetch movie using parameters (filters) in kwargs
            # Use limit and order with default values
            # Return list of Movie objects
            # If there is no matching result, return empty list ([])

         def save(self):
            # if self.pk is present, update database with current values
            # if it is new object, insert into database
            # add "RETURNING id" to sql if you need pk after execution (see Movie)
            # Return call to get method:
            return Movie.get(identifier=self.identifier)

         def delete(self):
            # If object is not populated from database, ie. self.pk is None:
            raise ValueError("Movie is not saved yet.")
            # Delete Movie using identifier from database.
            # Do not return anything

* `__init__` section of object should take parameters in same order as in schema.sql file.
* After creating model add it to lightmdb/models/__init__.py file.

**Create Form for each Model**:

* In order to safely create Model using user's request parameters create Form based on Model.
* Forms should be under lightmdb/forms/ folder.
* After creating form add it to lightmdb/forms/__init__.py file.

**Creating View**:

* To show your new model in client you will need add view for it.
* Create view file under lightmdb/views/ folder.
* Make Blueprint variable for you view, add all views for that Blueprint.
* Add your Blueprint variable to lightmdb/views/__init__.py file.

**Add view to urls**:

* In order to enable views we need to add them in lightmdb/application.py file.
* Add your new view to `DEFAULT_BLUEPRINTS` parameter.
* Run server and check your view

**Writing Tests**:

CI will test project in each pull request using /tests.py file. Add your new model and view tests in that file.


Work done by each team member:
------------------------------
List with issues for each team member can be found on `Github Projects <https://github.com/itucsdb1630/itucsdb1630/projects/1>`_

.. toctree::

   member1
   member2
   member3
   member4
   member5
