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
        STATIC_ROOT = "/path/to/static/root/static/"
    ```
    Additional Apache wsgi_mod configuration needed.
    

4. Run the migrations if needed (this checks if there was any db schema alteration and applies it to the database you specified on the local_settings.py module):
    ```sh
        $ python riscoplatform/manage.py migrate
    ```

5. Collect static files (only for deployment):
    ```sh
        $ python riscoplatform/manage.py collectstatic
    ```
    And restart Apache
    
6. If you want to use a prefix after the domain url you have to change the riscoplatform/static/base_url.js and replace with your prefix:
    ```js
        var BASE_URL = '/your-prefix';
    ```
    And restart Apache
    
7. Run development servers (only for development):
    ```sh
        $ python riscoplatform/manage.py runserver
    ```
    
    
### Update the app in production

1. Pull the repositoty;
2. Repeat the steps 2, 4 and 5.
    
