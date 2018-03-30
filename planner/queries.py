from planner import services
from planner.models import CulturalOperation, COWithDate, COWithOffset, ForthcomingOperation, CultivatedArea, Garden, \
    History, HistoryItem
from datetime import datetime, timedelta, date


def get_alert_within_notification_period(garden_id, notification_delay):
    """ Return an array with the active alerts and their due date
     Based on the undone alerts, their original cultural operation and en eventual postponement
     """
    future_alerts = get_future_alerts(garden_id)
    past_alerts = get_past_alerts(garden_id)
    time_delta = date.today() + timedelta(days=notification_delay)
    todo = []
    for a in future_alerts:
        if services.get_due_date(a, past_alerts) < time_delta:
            todo.append(a)
    return sorted(todo, key=get_operation_due_date)


def get_currently_active_alerts(garden_id):
    """ Return the list of active alerts for the garden with id garden_id.
    An alert is considered as active if it is marked as notdone and the due date is within the notification delay of the garden """
    notification_delay = Garden.objects.get(pk=garden_id).notification_delay
    return get_alert_within_notification_period(garden_id, notification_delay)


def get_past_alerts(garden_id):
    return ForthcomingOperation.objects.filter(area_concerned__in=get_garden_areas(garden_id), is_done=True)


def get_future_alerts(garden_id):
    return ForthcomingOperation.objects.filter(area_concerned__in=get_garden_areas(garden_id), is_done=False)


def done_alerts(garden_id):
    """ Return the list of alerts of this garden that are marked as done """
    # garden_areas = get_garden_areas(garden_id)
    history = HistoryItem.objects.order_by('-execution_date').select_subclasses().filter(
        history=services.get_current_history(garden_id))
    return history


def get_garden_areas(garden_id):
    """ Return the active garden's areas of the garden """
    return CultivatedArea.objects.filter(garden_id=garden_id, is_active=True)


def get_operation_due_date(forthcomingoperation):
    garden_areas = get_garden_areas(forthcomingoperation.area_concerned.surface.garden.id)
    alert_history = ForthcomingOperation.objects.filter(area_concerned__in=garden_areas, is_done=True)
    computed_due_date = services.get_due_date(forthcomingoperation, alert_history)
    return computed_due_date
