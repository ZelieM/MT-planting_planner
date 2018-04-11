from django.test import TestCase

from planner.models import Garden
from planner.queries import done_alerts


class QueriesTests(TestCase):

    def setUp(self):
        garden = Garden.objects.create(name="MyGarden", postal_code=1000)

    def test_done_alerts(self):
        self.assertEqual(len(done_alerts(Garden.objects.get(name="MyGarden").id)), 0)
