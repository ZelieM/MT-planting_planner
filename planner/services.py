from datetime import timedelta
from planner.models import CulturalOperation, Alerts, COWithDate, COWithOffset
from planner.templatetags.planner_extras import register


def add_initial_operation_to_alerts(cultivated_area, date):
    """ Add the initial operation of the vegetable seeded in cultivated_area to the list of alerts.
    The initial operation is marked as done with execution_date=date.
    The list of operations related to the same vegetable are added as undone to the list of alerts """
    vegetable_seeded = cultivated_area.vegetable_id
    initial_co = CulturalOperation.objects.select_subclasses().get(vegetable_id=vegetable_seeded, is_initial=True)
    # TODO take duration into account
    # Add the initial operation as "done"
    Alerts.objects.create(area_concerned=cultivated_area, original_cultural_operation=initial_co, execution_date=date,
                          done=True)
    # All the operation relative to this vegetable are added to alerts
    for co in CulturalOperation.objects.select_subclasses().filter(vegetable_id=vegetable_seeded, is_initial=False):
        Alerts.objects.create(area_concerned=cultivated_area, original_cultural_operation=co)


@register.filter
def get_due_date(alert, alert_history):
    """ Return the due date of the alert, knowing the alert history (due date is computed from
    previous operations in history for cultural operations with offset """
    original_operation = CulturalOperation.objects.select_subclasses().get(pk=alert.original_cultural_operation_id)
    if isinstance(original_operation, COWithDate):
        return original_operation.get_date()
    elif isinstance(original_operation, COWithOffset):
        previous_operation = alert_history.get(original_cultural_operation=original_operation.previous_operation)
        # We check if the previous operation is already done
        if previous_operation:
            return previous_operation.execution_date + timedelta(days=original_operation.offset_in_days)
        else:
            return original_operation.get_date()

