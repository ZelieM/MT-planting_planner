from django.contrib.auth.decorators import permission_required


def researcher_permission_required():
    """
    Custome decorator for researcher with a login url set based on this application
    """
    return permission_required('research.is_researcher', login_url="/login/")
