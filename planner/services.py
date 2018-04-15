from datetime import timedelta, date

from planner.models import CulturalOperation, ForthcomingOperation, COWithOffset, Operation, History, \
    HistoryItem, Bed, CultivatedArea
from planner.templatetags.planner_extras import register


def add_new_plantation_to_alerts(garden, vegetable_id, label, surface_id):
    """ Create a cultivated area on the surface surface_id with the vegetable vegetable_id and with a label.
    The list of operations related to this vegetable are added as undone to the list of alerts
    Return true if the plantation has been added successfully and False if an existing plantation already existed on
    the same surface and with the same label and vegetable """

    if CultivatedArea.objects.filter(vegetable_id=vegetable_id, label=label, surface_id=surface_id, is_active=True):
        return False  # There is already a cultivated area with all the same properties
    else:
        cultivated_area = CultivatedArea.objects.create(garden=garden, vegetable_id=vegetable_id,
                                                        label=label, surface_id=surface_id)
        vegetable_seeded = cultivated_area.vegetable_id
        # All the operation relative to this vegetable are added to alerts
        for co in CulturalOperation.objects.select_subclasses().filter(vegetable_id=vegetable_seeded):
            ForthcomingOperation.objects.create(area_concerned=cultivated_area, original_cultural_operation=co)
        return True


@register.filter
def get_due_date(alert, alert_history):
    """ Return the due date of the alert, knowing the alert history (due date is computed from
    previous operations in history for cultural operations with offset """
    original_operation = CulturalOperation.objects.select_subclasses().get(pk=alert.original_cultural_operation_id)
    postpone = alert.postponement
    if isinstance(original_operation, COWithOffset) and alert_history:
        try:
            # We check if the previous operation is already done
            previous_operation = alert_history.get(area_concerned=alert.area_concerned,
                                                   original_cultural_operation=original_operation.previous_operation)
            return previous_operation.execution_date + timedelta(days=original_operation.offset_in_days + postpone)

        except ForthcomingOperation.DoesNotExist:
            return original_operation.get_date() + timedelta(days=postpone)
    else:  # Case of an COWithDate operation or an empty alert_history
        return original_operation.get_date() + timedelta(days=postpone)


def mark_operation_as_done(operation_id, execution_date, executor, duration, note=""):
    """ Mark an alert as done with and execution date and an executor """
    alert = ForthcomingOperation.objects.get(pk=operation_id)
    alert.execution_date = execution_date
    alert.is_done = True
    alert.save()
    garden_id = alert.area_concerned.surface.garden_id
    history = get_current_history(garden_id)
    operation_name = alert.original_cultural_operation.name
    Operation.objects.create(execution_date=execution_date, executor=executor, area_concerned=alert.area_concerned,
                             name=operation_name, history=history, original_alert_id=operation_id, note=note,
                             duration=duration)


def postpone_alert(alert_id, postponement):
    """ Postpone an alert by the number of days passed as argument """
    alert = ForthcomingOperation.objects.get(pk=alert_id)
    alert.postponement = alert.postponement + int(postponement)
    alert.save()


def delete_operation_with_reason(operation_id, executor, reason, note=""):
    """ Delete an alert and eventually all the futures alerts relative to this cultivated_area"""
    alert = ForthcomingOperation.objects.get(pk=operation_id)
    if reason == "destruction":
        alerts_to_delete = ForthcomingOperation.objects.filter(area_concerned=alert.area_concerned, is_done=False)
        for a in alerts_to_delete:
            mark_operation_as_deleted(a, executor, note)
    else:
        mark_operation_as_deleted(alert, executor, note)


def mark_operation_as_deleted(operation, executor, note=""):
    garden_id = operation.area_concerned.surface.garden_id
    history = get_current_history(garden_id)
    operation_name = operation.original_cultural_operation.name
    Operation.objects.create(execution_date=date.today(), executor=executor, area_concerned=operation.area_concerned,
                             name=operation_name, history=history, is_deletion=True, original_alert=operation,
                             note=note)
    operation.is_done = True
    operation.execution_date = date.today()
    operation.save()


def get_current_history(garden_id):
    try:
        history = History.objects.get(garden_id=garden_id)
        return history
    except History.DoesNotExist:
        # If this garden doesn't have an active history, create a new one
        return History.objects.create(garden_id=garden_id)


def get_history_items(history_id):  # pragma: no cover
    return HistoryItem.objects.select_subclasses().filter(history_id=history_id)


def get_history_operations(history_id):  # pragma: no cover
    return Operation.objects.filter(history_id=history_id, area_concerned__isnull=False)


def add_new_operation_to_alerts(operation):
    """ In the case a new operation is added to a vegetable, this operation must be added to all the
    currently active CultivatedArea that have this vegetable seeded """
    vegetable_concerned = operation.vegetable
    areas_concerned = ForthcomingOperation.objects.filter(area_concerned__vegetable=vegetable_concerned,
                                                          area_concerned__is_active=True).values(
        'area_concerned').distinct('area_concerned')
    for a in areas_concerned:
        area_id = a.get('area_concerned')
        ForthcomingOperation.objects.create(original_cultural_operation=operation, area_concerned_id=area_id)


def get_expected_duration(operation):
    """ Get the expected duration of an operation based on the data of the model"""
    area = operation.area_concerned.surface.id
    area_size = Bed.objects.get(pk=area).get_area
    unitary_time_needed = operation.original_cultural_operation.duration
    return area_size * unitary_time_needed


def deactivate_cultivated_area(area_id, user):
    area_concerned = CultivatedArea.objects.get(pk=area_id)
    area_concerned.is_active = False
    area_concerned.save()
    note = "La culture a été marquée comme terminée avant que cette opération ne soit réalisée"
    for op in ForthcomingOperation.objects.filter(area_concerned=area_concerned, is_done=False):
        mark_operation_as_deleted(op, user, note=note)
