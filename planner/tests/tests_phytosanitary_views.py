from django.contrib.auth.models import User
from django.test import TestCase, Client

from planner.models import Garden, Vegetable, Parcel, Bed, CultivatedArea


class PhytosanitaryViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = 'test_user'
        self.email = 'test@whatever.com'
        self.password = 'test'
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.garden = Garden.objects.create(name="MyGarden", postal_code=1000)
        self.garden.users.add(self.user)
        self.vegetable = Vegetable.objects.create(name="Tomato", variety="Yellow Pearshaped", garden=self.garden)
        self.parcel = Parcel.objects.create(name="MyParcel", garden_id=self.garden.id)
        self.surface = Bed.objects.create(name="Bedding", garden=self.garden, parcel=self.parcel, width=250, length=250)
        self.area = CultivatedArea.objects.create(vegetable=self.vegetable, garden=self.garden, label="Tomato area",
                                                  surface=self.surface)

    def test_index(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/{}/phytosanitaire'.format(self.garden.id))
        self.assertEqual(response.status_code, 200)

    def test_create_phytosanitaire(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/{}/create_phytosanitaire'.format(self.garden.id))
        self.assertEqual(response.status_code, 200)
        form = {'commercial_name': "TOXIC", 'quantity': '10.111', 'unity': 'l', 'receipt_date': '2018-04-20',
                'supplier': '01245'}
        self.assertEqual(len(self.garden.incomingphytosanitaire_set.all()), 0)
        response = self.client.post('/{}/create_phytosanitaire'.format(self.garden.id), form)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(self.garden.incomingphytosanitaire_set.all()), 1)

    def test_create_phytosanitaire_usage(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/{}/create_phytosanitaire_usage'.format(self.garden.id))
        self.assertEqual(response.status_code, 200)
        form = {'commercial_name': 'Toxic', 'usage_date': '2018-04-10', 'dose_used': '10.123', 'unity': 'kg',
                'crop_treated': self.area.id, 'comment': ''}
        self.assertEqual(len(self.garden.phytosanitaireusage_set.all()), 0)
        response = self.client.post('/{}/create_phytosanitaire_usage'.format(self.garden.id), form)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(self.garden.phytosanitaireusage_set.all()), 1)
