from datetime import datetime, date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase

from planner import queries
from planner.models import Garden, Vegetable, COWithDate, ForthcomingOperation, CultivatedArea, Area, COWithOffset, \
    Operation, Bed


class ServicesTests(TestCase):

    def setUp(self):
        garden = Garden.objects.create(name="MyGarden")
        surface1 = Area.objects.create(garden=garden, area_surface=200)
        v1 = Vegetable.objects.create(name="Carrots", garden=garden)
        op1 = COWithDate.objects.create(name="FirstOP", vegetable=v1, absoluteDate=date(2017, 12, 6))
        COWithDate.objects.create(name="SecondOP", vegetable=v1, absoluteDate=date(2017, 10, 8))
        CultivatedArea.objects.create(vegetable=v1,
                                      production_period=queries.services.get_current_production_period(garden.id),
                                      label='area1', surface=surface1)
        COWithOffset.objects.create(name="OffsetOp", vegetable=v1, previous_operation=op1, offset_in_days=5)

    def test_get_due_date(self):
        """ Test the function services.get_due_date(alert, alert_history) """
        alert_history_empty = ForthcomingOperation.objects.filter(is_done=True)
        my_alert1 = ForthcomingOperation.objects.create(area_concerned=CultivatedArea.objects.get(label="area1"),
                                                        original_cultural_operation=COWithDate.objects.get(
                                                            name="FirstOP"))
        computed_date = queries.services.get_due_date(my_alert1, alert_history_empty)
        supposed_date = date(2017, 12, 6)
        self.assertEqual(computed_date, supposed_date)
        my_alert2 = ForthcomingOperation.objects.create(area_concerned=CultivatedArea.objects.get(label="area1"),
                                                        original_cultural_operation=COWithOffset.objects.get(
                                                            name="OffsetOp"))
        computed_date = queries.services.get_due_date(my_alert2, alert_history_empty)
        self.assertEqual(computed_date, date(2017, 12, 11))  # offset : 5 days, previous operation : 6/12/2017
        my_alert1.execution_date = date(2017, 12, 12)
        my_alert1.is_done = True
        my_alert1.save()
        alert_history_not_empty = ForthcomingOperation.objects.filter(is_done=True)
        computed_date = queries.services.get_due_date(my_alert2, alert_history_not_empty)
        supposed_date = date(2017, 12, 17)  # offset5 days and execution date : 12/12/2017
        self.assertEqual(computed_date, supposed_date)

    def test_mark_alert_as_done(self):
        alert = ForthcomingOperation.objects.create(area_concerned=CultivatedArea.objects.get(label="area1"),
                                                    original_cultural_operation=COWithDate.objects.get(name="SecondOP"))
        self.assertFalse(alert.is_done)
        queries.services.mark_alert_as_done(alert_id=alert.id, execution_date=date(2017, 10, 10), executor=None,
                                            note=None, duration=None)
        self.assertTrue(ForthcomingOperation.objects.get(pk=alert.id).is_done)

    def test_postpone_alert(self):
        alert = ForthcomingOperation.objects.create(area_concerned=CultivatedArea.objects.get(label="area1"),
                                                    original_cultural_operation=COWithDate.objects.get(name="SecondOP"))
        alert_history = ForthcomingOperation.objects.filter(is_done=True)
        self.assertEqual(queries.services.get_due_date(alert, alert_history), date(2017, 10, 8))
        queries.services.postpone_alert(alert.id, 8)
        alert_postponed = ForthcomingOperation.objects.get(pk=alert.id)
        self.assertEqual(queries.services.get_due_date(alert_postponed, alert_history), date(2017, 10, 16))

    def test_mark_alert_as_deleted(self):
        alert = ForthcomingOperation.objects.create(area_concerned=CultivatedArea.objects.get(label="area1"),
                                                    original_cultural_operation=COWithDate.objects.get(name="SecondOP"))
        self.assertFalse(alert.is_done)
        queries.services.mark_alert_as_deleted(alert, executor=None)
        self.assertTrue(ForthcomingOperation.objects.get(pk=alert.id).is_done)
        self.assertEqual(alert.execution_date, date.today())
        operation_in_history = Operation.objects.get(original_alert=alert)
        self.assertEqual(operation_in_history.execution_date, date.today())
        self.assertEqual(operation_in_history.area_concerned, CultivatedArea.objects.get(label="area1"))
        self.assertTrue(operation_in_history.is_deletion)

    def test_delete__useless_alert(self):
        # Only one alert is deleted
        alert = ForthcomingOperation.objects.create(area_concerned=CultivatedArea.objects.get(label="area1"),
                                                    original_cultural_operation=COWithDate.objects.get(name="SecondOP"))
        self.assertFalse(alert.is_done)
        queries.services.delete_alert(alert.id, executor=None, reason="useless")
        self.assertTrue(ForthcomingOperation.objects.get(pk=alert.id).is_done)
        operation_in_history = Operation.objects.get(original_alert=alert)
        self.assertTrue(operation_in_history.is_deletion)
        self.assertEqual(operation_in_history.execution_date, date.today())
        self.assertEqual(operation_in_history.area_concerned, CultivatedArea.objects.get(label="area1"))

    def test_delete_destruction_alert(self):
        # All subsequent alerts must be deleted
        area = CultivatedArea.objects.get(label="area1")
        alert = ForthcomingOperation.objects.create(area_concerned=area,
                                                    original_cultural_operation=COWithDate.objects.get(name="FirstOP"))
        ForthcomingOperation.objects.create(area_concerned=area,
                                                        original_cultural_operation=COWithDate.objects.get(
                                                            name="SecondOP"))
        ForthcomingOperation.objects.create(area_concerned=area,
                                                        original_cultural_operation=COWithOffset.objects.get(
                                                            name="OffsetOp"))
        queries.services.delete_alert(alert.id, executor=None, reason="destruction")
        for a in ForthcomingOperation.objects.filter(area_concerned=area):
            self.assertTrue(a.is_done)
            self.assertTrue(Operation.objects.get(original_alert=a).is_deletion)

    def test_add_initial_operation_to_alerts(self):
        vegetable = self.create_vegetable_with_alerts()
        surface = Bed.objects.create(name="MySurface", garden_id=vegetable.garden_id, length=150, width=250)
        area = CultivatedArea.objects.create(vegetable=vegetable,
                                      production_period=queries.services.get_current_production_period(vegetable.garden_id),
                                      label='area2', surface=surface)
        with self.assertRaises(ForthcomingOperation.DoesNotExist):
            ForthcomingOperation.objects.get(area_concerned=area)
        user = User.objects.create(username="SuperUser", email="super@super.com", password="azerty")
        user.garden_set.add(vegetable.garden)
        queries.services.add_initial_operation_to_alerts(area, execution_date=date.today(), user=user)
        self.assertEqual(len(ForthcomingOperation.objects.filter(area_concerned=area)), 3)
        self.assertTrue(ForthcomingOperation.objects.get(original_cultural_operation=COWithDate.objects.get(name="Seeding")).is_done)
        self.assertFalse(ForthcomingOperation.objects.get(
            original_cultural_operation=COWithDate.objects.get(name="Work")).is_done)
        self.assertFalse(ForthcomingOperation.objects.get(
            original_cultural_operation=COWithOffset.objects.get(name="Next")).is_done)

    def create_vegetable_with_alerts(self):
        v2 = Vegetable.objects.create(name="Cucumber", garden=Garden.objects.get(name="MyGarden"))
        COWithDate.objects.create(vegetable=v2, absoluteDate=date(2018, 2, 15), is_initial=True, name="Seeding")
        second = COWithDate.objects.create(vegetable=v2, absoluteDate=date(2018, 4, 15), name="Work")
        COWithOffset.objects.create(vegetable=v2, name="Next", previous_operation=second, offset_in_days=15)
        return v2