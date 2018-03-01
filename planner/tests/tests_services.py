from datetime import datetime, date, timedelta

from django.test import TestCase

from planner import services, queries
from planner.models import Garden, Vegetable, COWithDate, Alerts, CultivatedArea, Area, COWithOffset


class ServicesTests(TestCase):

    def setUp(self):
        garden = Garden.objects.create(name="MyGarden")
        surface1 = Area.objects.create(garden=garden, area_surface=200)
        v1 = Vegetable.objects.create(name="Carrots")
        # v2 = Vegetable.objects.create(name="Cucumber")
        op1 = COWithDate.objects.create(name="FirstOP", vegetable=v1, absoluteDate=date(2017, 12, 6))
        CultivatedArea.objects.create(vegetable=v1, production_period=queries.get_current_production_period(garden.id),
                                      label='area1', surface=surface1)
        COWithOffset.objects.create(name="OffsetOp", vegetable=v1, previous_operation=op1, offset_in_days=5)

    def test_get_due_date(self):
        """ Test the function services.get_due_date(alert, alert_history) """
        alert_history_empty = Alerts.objects.filter(done=True)
        my_alert1 = Alerts.objects.create(area_concerned=CultivatedArea.objects.get(pk=1),
                                          original_cultural_operation=COWithDate.objects.get(name="FirstOP"))
        computed_date = services.get_due_date(my_alert1, alert_history_empty)
        supposed_date = date(2017, 12, 6)
        self.assertEqual(computed_date, supposed_date)
        my_alert2 = Alerts.objects.create(area_concerned=CultivatedArea.objects.get(pk=1),
                                          original_cultural_operation=COWithOffset.objects.get(name="OffsetOp"))
        computed_date = services.get_due_date(my_alert2, alert_history_empty)
        self.assertEqual(computed_date, date(2017, 12, 11))  # offset : 5 days, previous operation : 6/12/2017
        my_alert1.execution_date = date(2017, 12, 12)
        my_alert1.done = True
        my_alert1.save()
        alert_history_not_empty = Alerts.objects.filter(done=True)
        computed_date = services.get_due_date(my_alert2, alert_history_not_empty)
        supposed_date = date(2017, 12, 17)  # offset5 days and execution date : 12/12/2017
        self.assertEqual(computed_date, supposed_date)
