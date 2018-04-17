from datetime import date, timedelta

from django.test import TestCase

from planner.models import Garden, CultivatedArea, Vegetable, Bed, COWithDate, COWithOffset, ForthcomingOperation
from planner.queries import done_alerts, get_currently_active_alerts

NOTIFICATION_DELAY = 8


class QueriesTests(TestCase):

    def setUp(self):
        self.garden = Garden.objects.create(name="MyGarden", postal_code=1000, notification_delay=NOTIFICATION_DELAY)
        self.vegetable = Vegetable.objects.create(name="Veggie", garden=self.garden)
        self.bed = Bed.objects.create(garden=self.garden, name="MyBed", width=500, length=500)
        self.plantation = CultivatedArea.objects.create(garden=self.garden, is_active=True, vegetable=self.vegetable,
                                                        surface=self.bed, label="VeggieInBed")
        self.secondplantation = CultivatedArea.objects.create(garden=self.garden, is_active=True, vegetable=self.vegetable,
                                                        surface=self.bed, label="SecondVeggieBed")

    def test_done_alerts(self):
        self.assertEqual(len(done_alerts(self.garden.id)), 0)

    def test_alerts_within_notification_period(self):
        self.assertEqual(len(get_currently_active_alerts(self.garden.id)), 0)
        op1 = COWithDate.objects.create(name="todayPlusThree", vegetable=self.vegetable,
                                        absoluteDate=date.today() + timedelta(days=3))
        # Necessary to add this newly created operation to the forthcoming operation
        ForthcomingOperation.objects.create(area_concerned=self.plantation, original_cultural_operation=op1)
        self.assertEqual(len(get_currently_active_alerts(self.garden.id)), 1)
        op2 = COWithDate.objects.create(name="todayPlusTen", vegetable=self.vegetable,
                                        absoluteDate=date.today() + timedelta(days=10))
        ForthcomingOperation.objects.create(area_concerned=self.plantation, original_cultural_operation=op2)
        self.assertEqual(len(get_currently_active_alerts(self.garden.id)), 1)
        op3 = COWithOffset.objects.create(name="op1PlusTwoDays", vegetable=self.vegetable, previous_operation=op1,
                                          offset_in_days=2)
        ForthcomingOperation.objects.create(area_concerned=self.plantation, original_cultural_operation=op3)
        self.assertEqual(len(get_currently_active_alerts(self.garden.id)), 2)

    def test_alerts_within_notification_period_by_area(self):
        self.assertEqual(len(get_currently_active_alerts(self.garden.id, self.secondplantation.id)), 0)
        op1 = COWithDate.objects.create(name="todayPlusThree", vegetable=self.vegetable,
                                        absoluteDate=date.today() + timedelta(days=3))
        ForthcomingOperation.objects.create(area_concerned=self.secondplantation, original_cultural_operation=op1)
        self.assertEqual(len(get_currently_active_alerts(self.garden.id, self.secondplantation.id)), 1)
        # Adding operation for the other plantation is no
        op1 = COWithDate.objects.create(name="todayPlusThree", vegetable=self.vegetable,
                                        absoluteDate=date.today() + timedelta(days=3))
        ForthcomingOperation.objects.create(area_concerned=self.plantation, original_cultural_operation=op1)
        self.assertEqual(len(get_currently_active_alerts(self.garden.id, self.secondplantation.id)), 1)