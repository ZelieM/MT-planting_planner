from django.contrib.auth.decorators import login_required


def custom_login_required(function=None, login_url="/login/"):
    """
    Custome decorator with a login url set based on this application
    """
    return login_required(function, login_url=login_url)
