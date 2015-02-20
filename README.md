# risco
risco web app - openquake in a web environment

### Installation

1. Clone this repository
2. Install the dependencies (a virtual environment is recomended):
    ```sh
    $ pip install -r requirements.txt
    ```

3. Set up django local settings. <br>
    If you want to use it for developement: <br>
    ```py
        #riscoplatform/riscoplatform/local_settings.py
    
        DEBUG = True
        TEMPLATE_DEBUG = True
        ALLOWED_HOSTS = []
        DATABASE = {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': 'db_name',
            'USER': 'user_name',
            'PASSWORD': 'password',
            'HOST': 'db_host',
            'PORT': '5432'
        }
        TILESTACHE_HOST = 'http://localhost:8080/'
        TEMPLATE_DIRS = ('riscoplatform/templates',)
    ```
    <br>
    And to deploy:
    ```py
        DEBUG = False
        TEMPLATE_DEBUG = False
        ALLOWED_HOSTS = ['.host.']
        DATABASE = {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': 'db_name',
            'USER': 'user_name',
            'PASSWORD': 'password',
            'HOST': 'db_host',
            'PORT': '5432'
        }
        TILESTACHE_HOST = 'host'
        STATIC_ROOT = "/path/to/static/root/static/"
    ```
    Additional Apache wsgi_mod configuration needed.
    
4. Set up tilestache local configuration:<br>
    Just copy the file tilestcahe/production_tilestache.cfg to tilestcahe/local_tilestache.cfg<br>
    Open the local_settings.cfg and change the lines:
    
    ```py
        ...
        "dbinfo": {
            "host": "db_host",
            "port": "5432",
            "user": "user_name",
            "database": "db_name",
            "password": "password"
        },
        ...
    ```
    If you want to use it for deployment just create a file called tilestache.wsgi with the following content:
    ```py
        import os, TileStache
        application = TileStache.WSGITileServer('/path/to/your/project/tilestache/local_tilestache.cfg')
    ```
    Additional Apache wsgi_mod configuration needed.

5. Run the migrations if needed (this checks if there was any db schema alteration and applies it to the database you specified on the local_settings.py module):
    ```sh
        $ python riscoplatform/manage.py migrate
    ```
    
6. Collect static files (only for deployment):
    ```sh
        $ python riscoplatform/manage.py collectstatic
    ```
    And restart Apache
    
7. Run development servers (only for development):
    ```sh
        $ python tilestache-server.py -c tilestcahe/local_tilestache.cfg
    ```
    ```sh
        $ python riscoplatform/manage.py runserver
    ```
    
    
### Update the app in production

1. Pull the repositoty;
2. Repeat the steps 2, 5 and 6.
    
