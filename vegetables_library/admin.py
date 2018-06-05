from django.contrib import admin

# Register your models here.
from vegetables_library.models import Species, Variety, OutOfCupSeeding, GroundSeeding, CulturalOperation, COWithDate, \
    COWithOffset

admin.site.register(Species)
admin.site.register(Variety)
admin.site.register(GroundSeeding)
admin.site.register(OutOfCupSeeding)
admin.site.register(CulturalOperation)
admin.site.register(COWithDate)
admin.site.register(COWithOffset)
