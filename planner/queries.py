from planner import services
from planner.models import CulturalOperation, ProductionPeriod, COWithDate, COWithOffset, \
    ForthcomingOperation, CultivatedArea, Garden, History, HistoryItem
from datetime import datetime, timedelta, date


def get_alert_within_notification_period(future_alerts, past_alerts, notification_delay):
    """ Return an array with the active alerts and their due date
     Based on the undone alerts, their original cultural operation and en eventual postponement
     """
    time_delta = date.today() + timedelta(days=notification_delay)
    todo = []
    for a in future_alerts:
        if services.get_due_date(a, past_alerts) < time_delta:
            todo.append(a)
    return todo


def get_currently_active_alerts(garden_id):
    """ Return the list of active alerts for the garden with id garden_id.
    An alert is considered as active if it is marked as notdone and the due date is within the notification delay of the garden """
    garden_areas = get_garden_areas(garden_id)
    notdone_alerts = ForthcomingOperation.objects.filter(area_concerned__in=garden_areas, is_done=False)
    past_alerts = ForthcomingOperation.objects.filter(area_concerned__in=garden_areas, is_done=True)
    notification_delay = Garden.objects.get(pk=garden_id).notification_delay
    return get_alert_within_notification_period(notdone_alerts, past_alerts, notification_delay)


def done_alerts(garden_id):
    """ Return the list of alerts of this garden that are marked as done """
    # garden_areas = get_garden_areas(garden_id)
    return HistoryItem.objects.select_subclasses().filter(history=services.get_current_history(garden_id))


def get_garden_areas(garden_id):
    """ Return the garden's areas of the current production period of the garden """
    return CultivatedArea.objects.filter(production_period=services.get_current_production_period(garden_id),
                                         is_active=True)
