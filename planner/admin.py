from django.contrib import admin

from .models import Garden, Bed, Vegetable, ProductionPeriod, CulturalOperation, COWithDate, COWithOffset

admin.site.register(Garden)
admin.site.register(Bed)
admin.site.register(Vegetable)
admin.site.register(ProductionPeriod)
admin.site.register(CulturalOperation)
admin.site.register(COWithOffset)
admin.site.register(COWithDate)
