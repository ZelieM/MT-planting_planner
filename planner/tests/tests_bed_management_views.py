from django.contrib.auth.models import User
from django.test import TestCase, Client

from planner.models import Garden


class BedManagementViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = 'test_user'
        self.email = 'test@whatever.com'
        self.password = 'test'
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.garden = Garden.objects.create(name="MyGarden", postal_code=1000)
        self.garden.users.add(self.user)

    def test_beds_index(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get('/{}/'.format(self.garden.id))
        self.assertEqual(response.status_code, 200)

    def test_create_bed(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get('/{}/create_bed'.format(self.garden.id))
        self.assertEqual(response.status_code, 200)
        # Creating a bed
        self.assertEqual(len(self.garden.bed_set.all()), 0)
        form = {'name': 'MyBed', 'length': '450', 'width': '350', 'exposition': 'NO', 'comment': 'nocomment',
                'soil_type': 'oily'}
        response = self.client.post('/{}/create_bed'.format(self.garden.id), form)
        self.assertRedirects(response, expected_url='/{}/'.format(self.garden.id), status_code=302,
                             target_status_code=200)
        self.assertEqual(len(self.garden.bed_set.all()), 1)
