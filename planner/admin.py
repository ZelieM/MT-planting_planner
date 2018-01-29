from django.contrib import admin

from .models import Garden, Bed, Vegetable

admin.site.register(Garden)
admin.site.register(Bed)
admin.site.register(Vegetable)