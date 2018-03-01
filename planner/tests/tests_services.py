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
        op1 = COWithDate.objects.create(name="FirstOP", vegetable=v1, absoluteDate=date.today())
        CultivatedArea.objects.create(vegetable=v1, production_period=queries.get_current_production_period(garden.id),
                                      label='area1', surface=surface1)
        COWithOffset.objects.create(name="OffsetOp", vegetable=v1, previous_operation=op1, offset_in_days=5)

    def test_get_due_date(self):
        """ Test the function services.get_due_date(alert, alert_history) """
        alert_history = Alerts.objects.filter(done=True)
        my_alert = Alerts.objects.create(area_concerned=CultivatedArea.objects.get(pk=1),
                                         original_cultural_operation=COWithDate.objects.get(name="FirstOP"))

        computed_date = services.get_due_date(my_alert, alert_history)
        supposed_date = date.today()
        self.assertEqual(computed_date, supposed_date)
        my_alert.execution_date = date.today()
        my_alert.done = True
        my_alert.save()
        alert_history = Alerts.objects.filter(done=True)
        my_alert = Alerts.objects.create(area_concerned=CultivatedArea.objects.get(pk=1),
                                         original_cultural_operation=COWithOffset.objects.get(name="OffsetOp"))
        supposed_date = date.today() + timedelta(days=5)
        computed_date = services.get_due_date(my_alert, alert_history)
        self.assertEqual(computed_date, supposed_date)
