from .defaults import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'planting_planner_db',
        'USER': 'postgres',
        'PASSWORD': 'azerty',
        'HOST': '',
        'PORT': '5432'
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
