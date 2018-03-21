from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.filter
def get_garden_users(garden):
    return User.objects.filter(garden=garden)