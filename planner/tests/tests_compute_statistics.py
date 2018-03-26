from datetime import date, timedelta

from django.test import TestCase

from planner import queries
from planner.compute_statistics import from_timedelta_to_hours, get_future_work_hours_by_week, get_max_operations_date
from planner.models import Garden, Vegetable, COWithDate, COWithOffset, Bed

OP1_NAME = "OP1"
OP2_NAME = "OP2"
OP3_NAME = "OP3"


class ComputeStatisticsTests(TestCase):

    def setUp(self):
        self.garden = Garden.objects.create(name="MyGarden")
        self.surface1 = Bed.objects.create(garden=self.garden, width=1000, length=2000)
        self.vegetable1 = Vegetable.objects.create(name="Carrots", garden=self.garden)
        self.op1_2018_3_12 = COWithDate.objects.create(name=OP1_NAME, vegetable=self.vegetable1, absoluteDate=date(2018, 3, 12),
                                                  duration=timedelta(hours=2))
        self.op2_2_days_later = COWithOffset.objects.create(name=OP2_NAME, vegetable=self.vegetable1, previous_operation=self.op1_2018_3_12,
                                                       offset_in_days=2,
                                                       duration=timedelta(hours=1))
        self.op3_2018_10_8 = COWithDate.objects.create(name=OP3_NAME, vegetable=self.vegetable1, absoluteDate=date(2018, 10, 8),
                                                  duration=timedelta(seconds=72))

        queries.services.add_new_plantation_to_alerts(production_period=queries.services.get_current_production_period(
            self.garden.id), label='area1', surface_id=self.surface1.id, vegetable_id=self.vegetable1.id)

    def test_get_hours_from_timedelta(self):
        delta1 = timedelta(days=3, hours=2)
        three_days_and_two_hours_in_hours = 74
        self.assertEqual(from_timedelta_to_hours(delta1), three_days_and_two_hours_in_hours)
        one_hour_in_seconds = 3600
        delta2 = timedelta(days=1, seconds=one_hour_in_seconds)
        one_day_and_one_hour_in_hours = 25
        self.assertEqual(from_timedelta_to_hours(delta2), one_day_and_one_hour_in_hours)

    def test_get_work_hours_by_week(self):
        expected_duration = {}

        week = COWithOffset.objects.get(name=OP2_NAME).get_date().isocalendar()[1]
        op1_2_work_hours_for_200_square_meters = 400
        op2_1_work_hour_for_200_square_meters = 200
        three_work_hour_for_200_square_meters = op1_2_work_hours_for_200_square_meters + \
                                                op2_1_work_hour_for_200_square_meters
        expected_duration[str(week)] = three_work_hour_for_200_square_meters

        week = COWithDate.objects.get(name=OP3_NAME).get_date().isocalendar()[1]
        op3_72_seconds_work_hour_for_200_square_meters = 4.0  # (72 / 3600) * 200
        expected_duration[str(week)] = op3_72_seconds_work_hour_for_200_square_meters

        x_axis, y_axis = get_future_work_hours_by_week(Garden.objects.get(name="MyGarden"))
        self.assertEqual(expected_duration, y_axis)

    def test_get_max_operations_date(self):
        futures_operations = queries.get_future_alerts(garden_id=self.garden.id)
        past_operation = []  # all operations are in the future

        expected_max_operations_date = date(2018, 10, 8)
        result_max_operations_date = get_max_operations_date(futures_operations, past_operation)

        self.assertEquals(expected_max_operations_date, result_max_operations_date)

    def test_get_mondays_of_weeks_between_two_dates(self):
        pass
        # todo