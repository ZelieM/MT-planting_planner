from planner.models import CulturalOperation, ProductionPeriod, CulturalOperationHistory, COWithDate, COWithOffset
from datetime import datetime, timedelta, date


def active_alerts(garden_id):
    history = CulturalOperationHistory.objects.filter(production_period=get_current_production_period(garden_id))
    original_operations = history.values('original_C_Operation')
    vegetables_seeded = CulturalOperation.objects.filter(id__in=original_operations).values('vegetable')
    return get_todo_operations(vegetables_seeded, history)


def get_todo_operations(vegetable_id, history):
    cultural_operations = CulturalOperation.objects.select_subclasses().filter(vegetable_id__in=vegetable_id)
    todo = []
    time_delta = date.today() + timedelta(days=5)
    for co in cultural_operations:
        if not history.filter(original_C_Operation=co.id):
            # If the operation is not done yet, we have to add it to the todos
            if isinstance(co, COWithDate) and co.get_date() < time_delta:
                todo.append(co)
            elif isinstance(co, COWithOffset):
                previous_operation = history.get(original_C_Operation=co.previous_operation)
                # We check if the previous operation is already done (and in the history)
                if previous_operation and previous_operation.date + timedelta(days=co.offset_in_days) < time_delta:
                    todo.append(co)
    return todo


def get_current_production_period(garden_id):
    if not ProductionPeriod.objects.filter(garden_id=garden_id):
        # If this garden doesn't have an active production period, create a new one starting now
        ProductionPeriod.objects.create(label="first_period", start_date=datetime.today(), garden_id=garden_id)
    # Take the latest production period of this garden, supposed still active
    return ProductionPeriod.objects.filter(garden_id=garden_id).latest('start_date')
