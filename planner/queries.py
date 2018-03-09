from planner.services import get_due_date
from planner.models import CulturalOperation, ProductionPeriod, COWithDate, COWithOffset, \
    ForthcomingOperation, CultivatedArea, Garden, History, HistoryItem
from datetime import datetime, timedelta, date


def get_currently_active_alerts(garden_id):
    """ Return the list of active alerts for the garden with id garden_id.
    An alert is considered as active if it is marked as notdone and the due date is within the notification delay of the garden """
    garden_areas = get_garden_areas(garden_id)
    notdone_alerts = ForthcomingOperation.objects.filter(area_concerned__in=garden_areas, is_done=False)
    past_alerts = ForthcomingOperation.objects.filter(area_concerned__in=garden_areas, is_done=True)
    notification_delay = Garden.objects.get(pk=garden_id).notification_delay
    return get_alert_within_notification_period(notdone_alerts, past_alerts, notification_delay)


def get_current_history(garden_id):
    production_period = get_current_production_period(garden_id)
    history = History.objects.get(production_period=production_period)
    if not history:
        # If this garden doesn't have an active history, create a new one
        return History.objects.create(production_period=production_period)
    else:
        return history


def done_alerts(garden_id):
    """ Return the list of alerts of this garden that are marked as done """
    garden_areas = get_garden_areas(garden_id)
    # return ForthcomingOperation.objects.filter(area_concerned__in=garden_areas, is_done=True).order_by('execution_date')
    return HistoryItem.objects.select_subclasses().filter(history=get_current_history(garden_id))


def get_alert_within_notification_period(future_alerts, past_alerts, notification_delay):
    """ Return an array with the active alerts and their due date
     Based on the undone alerts, their original cultural operation and en eventual postponement
     """
    time_delta = date.today() + timedelta(days=notification_delay)
    todo = []
    for a in future_alerts:
        if get_due_date(a, past_alerts) < time_delta:
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
    return CultivatedArea.objects.filter(production_period=get_current_production_period(garden_id), is_active=True)
