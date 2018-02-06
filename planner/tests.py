from django.test import TestCase

from .models import Garden


class GardenModelTests(TestCase):

    def setUp(self):
        Garden.objects.create(name="MyCuteGarden")
        Garden.objects.create(name="MyUglyGarden")

    def test_basic(self):
        g1 = Garden.objects.get(name="MyCuteGarden")
        g2 = Garden.objects.get(name="MyUglyGarden")
        self.assertNotEqual(g1.id, g2.id)
