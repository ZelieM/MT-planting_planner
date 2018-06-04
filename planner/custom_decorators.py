from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.utils.functional import wraps

from planner.models import Garden


def custom_login_required(function=None, login_url="/login"):
    """
    Custom decorator with a login url set based on this application
    """
    return login_required(function, login_url=login_url)


def access_private_garden(view):
    @wraps(view)
    @custom_login_required
    def inner(request, *args, **kwargs):
        # Get the Garden object
        garden = get_object_or_404(Garden, pk=kwargs['garden_id'])
        # Check and see if the logged in user can access this garden
        if request.user not in garden.users.all():
            return HttpResponseForbidden()
        return view(request, *args, **kwargs)
    return inner
