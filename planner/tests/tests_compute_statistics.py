from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase

from planner import queries
from planner.compute_statistics import from_timedelta_to_hours, get_future_work_hours_by_week
from planner.models import Garden, Vegetable, COWithDate, CultivatedArea, COWithOffset, Bed


class ComputeStatisticsTests(TestCase):

    def setUp(self):
        garden = Garden.objects.create(name="MyGarden")
        surface1 = Bed.objects.create(garden=garden, width=10, length=20)
        v1 = Vegetable.objects.create(name="Carrots", garden=garden)
        op1 = COWithDate.objects.create(name="OP1", vegetable=v1, absoluteDate=date(2018, 3, 12),
                                        duration=timedelta(hours=2))
        op2 = COWithOffset.objects.create(name="OP2", vegetable=v1, previous_operation=op1, offset_in_days=2,
                                          duration=timedelta(hours=1))
        op3 = COWithDate.objects.create(name="OP3", vegetable=v1, absoluteDate=date(2018, 10, 8),
                                        duration=timedelta(seconds=72))

        area = CultivatedArea.objects.create(vegetable=v1,
                                             production_period=queries.services.get_current_production_period(
                                                 garden.id),
                                             label='area1', surface=surface1)
        user = User.objects.create(username="SuperUser", email="super@super.com", password="azerty")
        queries.services.add_new_plantation_to_alerts(cultivated_area=area, user=user)

    def test_get_hours_from_timedelta(self):
        delta1 = timedelta(days=3, hours=2)
        self.assertEqual(from_timedelta_to_hours(delta1), 74)
        delta2 = timedelta(days=1, seconds=3600)
        self.assertEqual(from_timedelta_to_hours(delta2), 25)

    def test_get_work_hours_by_week(self):
        expected_duration = {}
        week = COWithOffset.objects.get(name="OP2").get_date().isocalendar()[1]
        expected_duration[str(week)] = 600.0
        week = COWithDate.objects.get(name="OP3").get_date().isocalendar()[1]
        expected_duration[str(week)] = 4.0
        self.assertEqual(expected_duration, get_future_work_hours_by_week(Garden.objects.get(name="MyGarden")))
