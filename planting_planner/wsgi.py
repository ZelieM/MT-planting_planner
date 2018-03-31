"""
WSGI config for planting_planner project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "planting_planner.settings.production")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
