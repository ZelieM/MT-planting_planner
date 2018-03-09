from django import template
from django.urls import reverse

from planner import services

from datetime import date, timedelta

from planner.models import Surface, Operation

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
    computed_due_date = services.get_due_date(alert, alert_history)
    return computed_due_date


@register.simple_tag
def days_late(due_date):
    today = date.today()
    delay = (today - due_date).days
    return delay


@register.simple_tag
def estimated_needed_time(alert):
    area = alert.area_concerned.surface.id
    area_size = Surface.objects.select_subclasses().get(pk=area)
    unitary_time_needed = alert.original_cultural_operation.duration
    return area_size.get_area() * unitary_time_needed


@register.filter
def is_operation(history_item):
    return type(history_item) is Operation
