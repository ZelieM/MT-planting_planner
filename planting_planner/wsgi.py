"""
WSGI config for planting_planner project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""


import os
import json
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = os.path.dirname(__file__)
key = os.path.join(BASE_DIR, "secrets.json")
with open(key) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secret=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)


SECRET_KEY = get_secret("SECRET_KEY")


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "planting_planner.settings.production")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()



