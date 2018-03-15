from datetime import timedelta, date, datetime

from planner.models import CulturalOperation, ForthcomingOperation, COWithDate, COWithOffset, Operation, History, \
    ProductionPeriod, HistoryItem, Surface, Vegetable
from planner.templatetags.planner_extras import register


def add_initial_operation_to_alerts(cultivated_area, execution_date, user):
    """ Add the initial operation of the vegetable seeded in cultivated_area to the list of alerts.
    The initial operation is marked as done with execution_date=date.
    The list of operations related to the same vegetable are added as undone to the list of alerts """
    vegetable_seeded = cultivated_area.vegetable_id
    initial_co = CulturalOperation.objects.select_subclasses().get(vegetable_id=vegetable_seeded, is_initial=True)
    # TODO take duration into account
    # Add the initial operation as "done"
    ForthcomingOperation.objects.create(area_concerned=cultivated_area, original_cultural_operation=initial_co,
                                        execution_date=execution_date, is_done=True)
    garden_id = cultivated_area.surface.garden_id
    history = History.objects.get(production_period=get_current_production_period(garden_id))
    Operation.objects.create(execution_date=execution_date, executor=user, area_concerned=cultivated_area,
                             name=initial_co.name, history=history)

    # All the operation relative to this vegetable are added to alerts
    for co in CulturalOperation.objects.select_subclasses().filter(vegetable_id=vegetable_seeded, is_initial=False):
        ForthcomingOperation.objects.create(area_concerned=cultivated_area, original_cultural_operation=co)


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


def mark_alert_as_done(alert_id, execution_date, executor, duration,  note=None):
    """ Mark an alert as done with and execution date and an executor """
    alert = ForthcomingOperation.objects.get(pk=alert_id)
    alert.execution_date = execution_date
    alert.is_done = True
    alert.save()
    garden_id = alert.area_concerned.surface.garden_id
    history = get_current_history(garden_id)
    operation_name = alert.original_cultural_operation.name
    Operation.objects.create(execution_date=execution_date, executor=executor, area_concerned=alert.area_concerned,
                             name=operation_name, history=history, original_alert_id=alert_id, note=note,
                             duration=duration)


def postpone_alert(alert_id, postponement):
    """ Postpone an alert by the number of days passed as argument """
    alert = ForthcomingOperation.objects.get(pk=alert_id)
    alert.postponement = alert.postponement + int(postponement)
    alert.save()


def delete_alert(alert_id, executor, reason, note=None):
    """ Delete an alert and eventually all the futures alerts relative to this cultivated_area"""
    alert = ForthcomingOperation.objects.get(pk=alert_id)
    if reason == "destruction":
        alerts_to_delete = ForthcomingOperation.objects.filter(area_concerned=alert.area_concerned, is_done=False)
        for a in alerts_to_delete:
            mark_alert_as_deleted(a, executor, note)
    else:
        mark_alert_as_deleted(alert, executor, note)


def mark_alert_as_deleted(alert, executor, note=None):
    garden_id = alert.area_concerned.surface.garden_id
    history = get_current_history(garden_id)
    operation_name = alert.original_cultural_operation.name
    Operation.objects.create(execution_date=date.today(), executor=executor, area_concerned=alert.area_concerned,
                             name=operation_name, history=history, is_deletion=True, original_alert=alert, note=note)

    alert.is_done = True
    alert.execution_date = date.today()
    alert.save()


def get_current_production_period(garden_id):
    """ Return the current, and thus active, production period of the garden with id garden_id """
    if not ProductionPeriod.objects.filter(garden_id=garden_id):
        # If this garden doesn't have an active production period, create a new one starting now
        ProductionPeriod.objects.create(label="first_period", start_date=datetime.today(), garden_id=garden_id)
    # Take the latest production period of this garden, supposed still active
    return ProductionPeriod.objects.filter(garden_id=garden_id).latest('start_date')


def get_current_history(garden_id):
    production_period = get_current_production_period(garden_id)
    try:
        history = History.objects.get(production_period=production_period)
        return history
    except History.DoesNotExist:
        # If this garden doesn't have an active history, create a new one
        return History.objects.create(production_period=production_period)


def get_history_items(history_id):
    return HistoryItem.objects.select_subclasses().filter(history_id=history_id)


def get_history_operations(history_id):
    return Operation.objects.filter(history_id=history_id, area_concerned__isnull=False)


def add_new_operation_to_alerts(operation):
    vegetable_concerned = operation.vegetable
    areas_concerned = ForthcomingOperation.objects.filter(area_concerned__vegetable=vegetable_concerned,
                                                          area_concerned__is_active=True).values(
        'area_concerned').distinct('area_concerned')
    for a in areas_concerned:
        area_id = a.get('area_concerned')
        ForthcomingOperation.objects.create(original_cultural_operation=operation, area_concerned_id=area_id)


def get_expected_duration(operation):
    area = operation.area_concerned.surface.id
    area_size = Surface.objects.select_subclasses().get(pk=area)
    unitary_time_needed = operation.original_cultural_operation.duration
    return area_size.get_area() * unitary_time_needed


def import_vegetables_to_garden(garden_id, vegetables_selected):
    from vegetables_library.models import Vegetable as library_vegetable
    for v in vegetables_selected:
        current_vegetable = library_vegetable.objects.get(pk=v)
        copy_vegetable(garden_id, current_vegetable)


def copy_vegetable(garden_id, vegetable_from_library):
    """ Copy a vegetable coming from the library to the garden's own library (with id garden_id)"""
    from vegetables_library.models import CulturalOperation as library_operation
    from vegetables_library.models import COWithOffset as library_co_with_offset
    from vegetables_library.models import COWithDate as library_co_with_date
    copied_vegetable = Vegetable.objects.create(garden_id=garden_id, name=vegetable_from_library.name)
    operations_to_copy = library_operation.objects.select_subclasses().filter(vegetable_id=vegetable_from_library.id)
    for op in operations_to_copy:
        if type(op) is library_co_with_date:
            co = COWithDate.objects.create(vegetable_id=copied_vegetable.id, name=op.name, duration=op.duration,
                                           is_initial=op.is_initial, absoluteDate=op.absoluteDate)
            co_with_offset_to_copy = library_co_with_offset.objects.filter(vegetable=vegetable_from_library, previous_operation=op)
            copy_with_recursion_co_with_offset(copied_vegetable.id, co_with_offset_to_copy, op, co)


def copy_with_recursion_co_with_offset(vegetable_concerned_id, operations_from_library_to_copy, library_parent_co,
                                       garden_parent_co):
    """ Copy a cultural operation with offset and all the cultural operation with offset depending on this one"""
    if not operations_from_library_to_copy:
        return None  # End of recursion
    for co_offset in operations_from_library_to_copy:
        new_garden_parent = copy_co_with_offset(vegetable_concerned_id, co_offset, garden_parent_co)
        from vegetables_library.models import COWithOffset as library_co_with_offset
        child_operations = library_co_with_offset.objects.filter(vegetable=library_parent_co.vegetable,
                                                                 previous_operation=co_offset)
        copy_with_recursion_co_with_offset(vegetable_concerned_id, child_operations, co_offset, new_garden_parent)


def copy_co_with_offset(vegetable_concerned_id, operation_to_copy, parent_co):
    """ Copy a cultural operation with offset from the library to a vegetable belonging to the garden"""
    return COWithOffset.objects.create(vegetable_id=vegetable_concerned_id, name=operation_to_copy.name,
                                       duration=operation_to_copy.duration,
                                       is_initial=operation_to_copy.is_initial, previous_operation=parent_co,
                                       offset_in_days=operation_to_copy.offset_in_days)
