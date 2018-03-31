from .defaults import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '130.104.12.56', 'lauzeplan.sipr.ucl.ac.be ']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lauzeplan',
        'USER': 'lauzeplan',
        'PASSWORD': 'Jd5uHTFg',
        'HOST': 'pgsql.uclouvain.be',
        'PORT': '5440'
    },
    'db_vegetables_library': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'vegetable_library_db',
        'USER': 'postgres',
        'PASSWORD': 'azerty',
        'HOST': '',
        'PORT': '5432'
    }
}