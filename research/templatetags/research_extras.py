

from django import template
from django.contrib.auth.models import User
from django.urls import reverse

register = template.Library()

@register.filter
def get_garden_users(garden):
    return User.objects.filter(garden=garden)

@register.simple_tag
def navactive(request, url):
    if request.path == reverse(url):
        return "active"
    return ""
