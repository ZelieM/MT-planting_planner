from django.contrib.auth.models import User
from django.test import TestCase, Client

from planner.models import Garden, Bed


class QRLogicViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = 'test_user'
        self.email = 'test@whatever.com'
        self.password = 'test'
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.garden = Garden.objects.create(name="MyGarden", postal_code=1000)
        self.garden.users.add(self.user)
        self.surface = Bed.objects.create(garden=self.garden, name="Bedding", length=250, width=250)

    def test_print_qr_index(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/{}/print_qr'.format(self.garden.id))
        self.assertEquals(response.get('Content-Type'), 'application/pdf')

    def test_bed_qr_view(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/{}/qr/{}'.format(self.garden.id, self.surface.id))
        self.assertEquals(response.status_code, 200)