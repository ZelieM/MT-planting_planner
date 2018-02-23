from django import template
from django.urls import reverse

from planner import services

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


@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@register.filter
def related_to(cultural_operation, vegetableid):
    return cultural_operation.select_subclasses().filter(vegetable_id=vegetableid).all()


@register.simple_tag
def due_date(alert, alert_history):
    date = services.get_due_date(alert, alert_history)
    return date
