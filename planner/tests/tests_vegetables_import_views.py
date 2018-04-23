from django.contrib.auth.models import User
from django.test import TestCase, Client

from planner.models import Garden, Bed


class ImportVegetablesViewsTests(TestCase):

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
        response = self.client.get('/{}/import_vegetables'.format(self.garden.id))
        self.assertEqual(response.status_code, 200)

    def test_select_vegetables(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/{}/import_vegetables/select'.format(self.garden.id))
        self.assertEqual(response.status_code, 200)
        from vegetables_library.models import Variety as library_vegetable
        from vegetables_library.models import Species as library_species
        species = library_species.objects.create(french_name="Red kuri")
        self.assertEqual(self.garden.vegetable_set.count(), 0)
        vegetable = library_vegetable.objects.create(french_name="Pumpkin", species=species)
        form = {'vegetables_id': vegetable.id}
        response = self.client.post('/{}/import_vegetables/select'.format(self.garden.id), form)
        self.assertRedirects(response, '/{}/import_vegetables'.format(self.garden.id))
        self.assertEqual(self.garden.vegetable_set.count(), 1)
