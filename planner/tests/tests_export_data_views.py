from django.contrib.auth.models import User
from django.test import TestCase, Client

from planner.models import Garden


class ExportDataViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = 'test_user'
        self.email = 'test@whatever.com'
        self.password = 'test'
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.garden = Garden.objects.create(name="MyGarden", postal_code=1000)
        self.garden.users.add(self.user)

    def test_index(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get('/{}/export'.format(self.garden.id))
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        login = self.client.login(username=self.username, password=self.password)
        form = {'first_date': '2018-04-15', 'end_date': '2018-05-01'}
        response = self.client.post('/{}/export_history'.format(self.garden.id), form)
        self.assertEquals(
            response.get('Content-Disposition'),
            "attachment; filename=history_from_2018-04-15.csv"
        )
        response = self.client.post('/{}/export_harvest'.format(self.garden.id), form)
        self.assertEquals(
            response.get('Content-Disposition'),
            "attachment; filename=harvest_history_from_2018-04-15.csv"
        )
        response = self.client.post('/{}/export_entry_register'.format(self.garden.id), form)
        self.assertEquals(
            response.get('Content-Disposition'),
            "attachment; filename=registre_entree_phytopharmaceutique_2018-04-15.csv"
        )
        response = self.client.post('/{}/export_usage_register'.format(self.garden.id), form)
        self.assertEquals(
            response.get('Content-Disposition'),
            "attachment; filename=registre_utilisation_phytopharmaceutique_2018-04-15.csv"
        )
