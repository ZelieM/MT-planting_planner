from planner import queries
from planner.models import Vegetable, CulturalOperation, CulturalOperationHistory


def add_initial_operation_to_history(garden_id, vegetable_id, date):
    # TODO deal with multiple adding: can't add two seeding of the same vegetable the same day (add label?)
    initial_co = CulturalOperation.objects.select_subclasses().get(vegetable_id=vegetable_id, is_initial=True)
    current_period = queries.get_current_production_period(garden_id)
    CulturalOperationHistory.objects.create(production_period=current_period, date=date,
                                            original_C_Operation=initial_co, duration=0, surface_processed=0)
