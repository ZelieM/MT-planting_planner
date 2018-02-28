from planner import services
from planner.models import CulturalOperation, ProductionPeriod, COWithDate, COWithOffset, \
    Alerts, CultivatedArea
from datetime import datetime, timedelta, date


NOTIFICATION_PERIOD = 5  # in days


def active_alerts(garden_id):
    """ Return the list of active alerts for the garden with id garden_id.
    An alert is considered as active if it is marked as notdone and the due date is within NOTIFICATION_PERIOD """
    garden_areas = get_garden_areas(garden_id)
    notdone_alerts = Alerts.objects.filter(area_concerned__in=garden_areas, done=False)
    past_alerts = Alerts.objects.filter(area_concerned__in=garden_areas, done=True)
    return from_alerts_get_due_dates(notdone_alerts, past_alerts)


def done_alerts(garden_id):
    """ Return the list of alerts of this garden that are marked as done """
    garden_areas = get_garden_areas(garden_id)
    return Alerts.objects.filter(area_concerned__in=garden_areas, done=True)


def from_alerts_get_due_dates(future_alerts, past_alerts):
    """ Return an array with the active alerts and their due date
     Based on the undone alerts, their original cultural operation and en eventual postponement
     """
    time_delta = date.today() + timedelta(days=NOTIFICATION_PERIOD)
    todo = []
    for a in future_alerts:
        if services.get_due_date(a, past_alerts) < time_delta:
            todo.append(a)
    return todo


def get_current_production_period(garden_id):
    """ Return the current, and thus active, production period of the garden with id garden_id """
    if not ProductionPeriod.objects.filter(garden_id=garden_id):
        # If this garden doesn't have an active production period, create a new one starting now
        ProductionPeriod.objects.create(label="first_period", start_date=datetime.today(), garden_id=garden_id)
    # Take the latest production period of this garden, supposed still active
    return ProductionPeriod.objects.filter(garden_id=garden_id).latest('start_date')


def get_garden_areas(garden_id):
    """ Return the garden's areas of the current production period of the garden """
    return CultivatedArea.objects.filter(production_period=get_current_production_period(garden_id))

