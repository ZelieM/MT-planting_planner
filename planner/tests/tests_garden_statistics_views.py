from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase, Client

from planner.models import Garden, History, Operation


class GardenStatisticsViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = 'test_user'
        self.email = 'test@whatever.com'
        self.password = 'test'
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.garden = Garden.objects.create(name="MyGarden", postal_code=1000)
        self.garden.users.add(self.user)


    def test_index(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/{}/statistics'.format(self.garden.id))
        self.assertEqual(response.status_code, 200)
