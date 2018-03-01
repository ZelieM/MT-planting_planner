from django.test import TestCase

from planner.models import Garden
from django.contrib.auth.models import User
from django.test import Client


class GardenModelTests(TestCase):

    def setUp(self):
        Garden.objects.create(name="MyCuteGarden")
        Garden.objects.create(name="MyUglyGarden")
        User.objects.create_user(username='john', password="smith", email="john@smith.com")

    def test_basic(self):
        g1 = Garden.objects.get(name="MyCuteGarden")
        g2 = Garden.objects.get(name="MyUglyGarden")
        self.assertNotEqual(g1.id, g2.id)

    def test_login_and_access(self):
        c = Client()
        response = c.get('/planner/garden_selection')
        self.assertEqual(response.status_code, 302)  # Access to garden selection not possible without login
        response = c.login(username='john', password='smith', email="john@smith.com")
        self.assertTrue(response)
        response = c.get('/planner/garden_selection')
        self.assertEqual(response.status_code, 200)

