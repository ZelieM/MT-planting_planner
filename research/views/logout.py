from django.contrib.auth import logout
from django.http import HttpResponseRedirect


def log_out(request):
    logout(request)
    return HttpResponseRedirect("/login/")