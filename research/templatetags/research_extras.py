from django import template
from django.contrib.auth.models import User
from django.urls import reverse

from vegetables_library.models import Variety

register = template.Library()


@register.simple_tag
def get_garden_number_users(garden):
    return len(User.objects.filter(garden=garden))


@register.simple_tag
def navactive(request, url):
    if request.path == reverse(url):
        return "active"
    return ""


@register.filter
def vegetable_operations(vegetableid):
    from vegetables_library.models import CulturalOperation
    return CulturalOperation.objects.select_subclasses().filter(vegetable_id=vegetableid).all()


@register.filter
def garden_vegetable_operations(vegetableid):
    from planner.models import CulturalOperation
    return CulturalOperation.objects.select_subclasses().filter(vegetable_id=vegetableid).all()


@register.filter
def varieties_from_species(species):
    return Variety.objects.filter(species=species)
