
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = [
    '.prise.fe.up.pt.',  # Also allow FQDN and subdomains
]

DATABASE = {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'riscodb',
        'USER': 'postgres',
        'PASSWORD': 'prisefeup',
        'HOST': 'priseDB.fe.up.pt',
        'PORT': '5432'
    }

EMAIL_HOST = 'prise.fe.up.pt'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = ''
EMAIL_PORT = 25
EMAIL_SUBJECT_PREFIX = 'Risco'



ADMINS = (
    ('Rui Barros', 'ruimsbarros08@gmail.com'),
)

TILESTACHE_HOST = 'http://prise.fe.up.pt/'

STATIC_ROOT = "/srv/apps/risco/risco/riscoplatform/static/"
