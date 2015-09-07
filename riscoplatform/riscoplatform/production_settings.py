DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = ['*',]
#ALLOWED_HOSTS = []
DATABASE = {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'riscodb_dev',
        'USER': 'postgres',
        'PASSWORD': 'prisefeup',
        'HOST': 'prisedb.fe.up.pt',
        'PORT': '5432'
    }

TEMPLATE_DIRS = ('/srv/apps/risco/risco/riscoplatform/riscoplatform/templates',)
STATICFILES_DIRS = ('/srv/apps/risco/risco/riscoplatform/riscoplatform/static',)
#STATICFILES_DIRS = ('/srv/static',)
#BASE_URL = 'risco/'
STATIC_ROOT = "/srv/www/static/"
LOGIN_URL = '/risco/accounts/login/'
LOGOUT_URL = '/risco/'
MEDIA_ROOT = '/srv/www/media/'
AVATAR_STORAGE_DIR = 'uploads/avatars'
LOGIN_REDIRECT_URL = '/risco/'
BASE_URL = '/'
