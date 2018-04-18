from django.contrib.auth.models import User
from django.test import TestCase, Client

from planner.models import Garden, Bed, Vegetable, CultivatedArea


class HistoryViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = 'test_user'
        self.email = 'test@whatever.com'
        self.password = 'test'
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.garden = Garden.objects.create(name="MyGarden", postal_code=1000)
        self.garden.users.add(self.user)
        surface = Bed.objects.create(garden=self.garden, name="MyBed", width=250, length=250)
        vegetable = Vegetable.objects.create(garden=self.garden, name="Carrot")
        self.carea = CultivatedArea.objects.create(garden=self.garden, surface=surface, vegetable=vegetable,
                                                   label="LetsHaveCarrotts")

    def test_add_punctual_operation_view(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get('/{}/alerts/add_punctual_operation'.format(self.garden.id))
        self.assertEqual(response.status_code, 200)
        form = {'execution_date': '2018-04-15', 'area_concerned': self.carea.id, 'name': 'Harvest',
                "duration": '00:00:15', 'note': 'this is a note'}
        response = self.client.post('/{}/alerts/add_punctual_operation'.format(self.garden.id), form)
        self.assertRedirects(response, '/{}/alerts'.format(self.garden.id))
        self.assertEqual(len(self.garden.history.historyitem_set.all()),1)

    def test_add_observation_view(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get('/{}/alerts/add_observation'.format(self.garden.id))
        self.assertEqual(response.status_code, 200)
        form = {'execution_date': '2018-04-15', 'area_concerned': self.carea.id, 'description': 'good job'}
        response = self.client.post('/{}/alerts/add_observation'.format(self.garden.id), form)
        self.assertRedirects(response, '/{}/alerts'.format(self.garden.id))
        self.assertEqual(len(self.garden.history.historyitem_set.all()), 1)
