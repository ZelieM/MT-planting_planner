from django.contrib.auth.models import User
from django.test import TestCase, Client

from planner.models import Garden


class VegetablesViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = 'test_user'
        self.email = 'test@whatever.com'
        self.password = 'test'
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.garden = Garden.objects.create(name="MyGarden", postal_code=1000)
        self.garden.users.add(self.user)

    def test_index_view(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/{}/vegetables'.format(self.garden.id))
        self.assertEqual(response.status_code, 200)

    def test_add_vegetable(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/{}/vegetables/new'.format(self.garden.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.garden.vegetable_set.all()), 0)
        form = {'name': 'Carrot', 'variety': 'Napoli'}
        response = self.client.post('/{}/vegetables/new'.format(self.garden.id), form)
        self.assertRedirects(response,'/{}/vegetables'.format(self.garden.id))
        self.assertEqual(len(self.garden.vegetable_set.all()),1)