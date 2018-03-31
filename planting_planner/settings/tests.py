from .dev import *

# Speed up tests by using sqlite engine
DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
DATABASES['db_vegetables_library']['ENGINE'] = 'django.db.backends.sqlite3'
