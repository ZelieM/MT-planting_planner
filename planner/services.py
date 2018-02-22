from planner import queries
from planner.models import Vegetable, CulturalOperation, CulturalOperationHistory, Alerts, CultivatedArea


def add_initial_operation_to_history(garden_id, vegetable_id, date):
    # TODO deal with multiple adding: can't add two seeding of the same vegetable the same day (add label?)
    initial_co = CulturalOperation.objects.select_subclasses().get(vegetable_id=vegetable_id, is_initial=True)
    current_period = queries.get_current_production_period(garden_id)
    CulturalOperationHistory.objects.create(production_period=current_period, date=date,
                                            original_C_Operation=initial_co, duration=0, surface_processed=0)


def add_initial_operation_to_alerts(cultivated_area, date):
    vegetable_seeded = cultivated_area.vegetable_id
    initial_co = CulturalOperation.objects.select_subclasses().get(vegetable_id=vegetable_seeded, is_initial=True)

    # TODO take duration into account
    # Add the initial operation as "done"
    Alerts.objects.create(area_concerned=cultivated_area,original_cultural_operation=initial_co, date=date, done=True)
    # All the operation relative to this vegetable are added to alerts
    for co in CulturalOperation.objects.select_subclasses().filter(vegetable_id=vegetable_seeded):
        Alerts.objects.create(area_concerned=cultivated_area, original_cultural_operation=co)

