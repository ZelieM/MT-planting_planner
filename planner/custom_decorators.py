from django.contrib.auth.decorators import login_required, permission_required


def custom_login_required(function=None, login_url="/login/"):
    """
    Custom decorator with a login url set based on this application
    """
    return login_required(function, login_url=login_url)

