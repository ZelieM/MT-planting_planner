from .dev import *

# Speed up tests by using sqlite engine
DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql'
DATABASES['db_vegetables_library']['ENGINE'] = 'django.db.backends.postgresql'
