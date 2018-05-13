from django import template
from django.urls import reverse

from planner import services, queries

from datetime import date, timedelta

from planner.models import Operation, ForthcomingOperation, CultivatedArea
from vegetables_library.models import Variety

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


@register.filter
def varieties_from_species(species):
    return Variety.objects.filter(species=species)


@register.simple_tag
def due_date(alert, garden_id):
    garden_areas = queries.get_garden_areas(garden_id)
    alert_history = ForthcomingOperation.objects.filter(area_concerned__in=garden_areas, is_done=True)
    computed_due_date = services.get_due_date(alert, alert_history)
    return computed_due_date


@register.simple_tag
def days_late(due_date):
    today = date.today()
    delay = (today - due_date).days
    return delay


@register.simple_tag
def estimated_needed_time(alert):
    return services.get_expected_duration(alert)


@register.simple_tag
def active_cultivated_areas(bed):
    return CultivatedArea.objects.filter(surface_id=bed, is_active=True)


@register.simple_tag
def inactive_cultivated_areas(bed):
    return CultivatedArea.objects.filter(surface_id=bed, is_active=False)


@register.simple_tag
def active_cultivated_vegetable(vegetable):
    return CultivatedArea.objects.filter(vegetable_id=vegetable, is_active=True)


@register.simple_tag
def inactive_cultivated_vegetable(vegetable):
    return CultivatedArea.objects.filter(vegetable_id=vegetable, is_active=False)

@register.simple_tag
def productivity(harvest_details):
    price = harvest_details.total_selling_price
    kg = harvest_details.kg_produced
    if price != 0 and kg != 0:
        return round(price/kg, 2)
    else:
        return 0


@register.filter
def is_operation(history_item):
    return type(history_item) is Operation
