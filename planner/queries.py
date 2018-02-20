from planner.models import CulturalOperation, ProductionPeriod
from datetime import datetime


def active_alerts(garden_id):
    cos = CulturalOperation.objects.select_subclasses().all()
    cos.filter()
    # print(cos)
    return cos


def get_current_production_period(garden_id):
    if not ProductionPeriod.objects.filter(garden_id=garden_id):
        # If this garden doesn't have an active production period, create a new one starting now
        ProductionPeriod.objects.create(label="first_period", start_date=datetime.today(), garden_id=garden_id)
    # Take the latest production period of this garden, supposed still active
    return ProductionPeriod.objects.filter(garden_id=garden_id).latest('start_date')
