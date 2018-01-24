from django import template
from django.urls import reverse

register = template.Library()


@register.filter
def divide(value, arg):
    try:
        return int(value) / int(arg)
    except (ValueError, ZeroDivisionError):
        return None


@register.simple_tag
def navactive(request, url, arg):
    if request.path == (reverse(url, args=[arg])):
        return "active"
    return ""
