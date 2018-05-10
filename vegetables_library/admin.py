from django.contrib import admin

# Register your models here.
from vegetables_library.models import Species, Variety, OutOfCupSeeding, GroundSeeding

admin.site.register(Species)
admin.site.register(Variety)
admin.site.register(GroundSeeding)
admin.site.register(OutOfCupSeeding)
