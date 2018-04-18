from django.contrib.auth.models import User
from django.test import TestCase, Client

from planner.models import Garden


class AlertsViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = 'test_user'
        self.email = 'test@whatever.com'
        self.password = 'test'
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.garden = Garden.objects.create(name="MyGarden", postal_code=1000)
        self.garden.users.add(self.user)

    def test_alert_view_index(self):
        response = self.client.get('/{}/alerts'.format(self.garden.id))
        self.assertRedirects(response, expected_url='/login/?next=/{}/alerts'.format(self.garden.id), status_code=302)
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get('/{}/alerts'.format(self.garden.id))
        self.assertEqual(response.status_code, 200)
