from .defaults import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '130.104.12.56', 'lauzeplan.sipr.ucl.ac.be ']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'planting_planner_db',
        'USER': 'vegetable_library_user',
        'PASSWORD': 'poprucapho',
        'HOST': '',
        'PORT': '5432',
    },
    'db_vegetables_library': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'vegetable_library_db',
        'USER': 'vegetable_library_user',
        'PASSWORD': 'poprucapho',
        'HOST': '',
        'PORT': '5432'
    }
}