from django.contrib.auth.models import User
from django.test import TestCase, Client

from planner.models import Garden, Bed, Parcel


class BedManagementViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = 'test_user'
        self.email = 'test@whatever.com'
        self.password = 'test'
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.garden = Garden.objects.create(name="MyGarden", postal_code=1000)
        self.parcel = Parcel.objects.create(name="MyParcel", garden=self.garden)
        self.garden.users.add(self.user)

    def test_beds_index(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get('/{}'.format(self.garden.id))
        self.assertEqual(response.status_code, 200)

    def test_create_parcel(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/{}/create_parcel'.format(self.garden.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.garden.parcel_set.all()), 1)
        form = {'name': 'SecondParcel'}
        response = self.client.post('/{}/create_parcel'.format(self.garden.id), form)
        self.assertRedirects(response, expected_url='/{}'.format(self.garden.id), status_code=302,
                             target_status_code=200)
        self.assertEqual(len(self.garden.parcel_set.all()), 2)

    def test_create_bed(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get('/{}/create_bed'.format(self.garden.id))
        self.assertEqual(response.status_code, 200)
        # Creating a bed
        self.assertEqual(len(self.garden.bed_set.all()), 0)
        form = {'parcel': self.parcel.id, 'name': 'MyBed', 'length': '450', 'width': '350', 'exposition': 'NO',
                'comment': 'nocomment', 'soil_type': 'oily'}
        response = self.client.post('/{}/create_bed'.format(self.garden.id), form)
        self.assertRedirects(response, expected_url='/{}'.format(self.garden.id), status_code=302,
                             target_status_code=200)
        self.assertEqual(len(self.garden.bed_set.all()), 1)

    def test_update_bed(self):
        bed = Bed.objects.create(garden=self.garden, name='FirstBed', width=250, length=250)
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get('/{}/update_bed/{}'.format(self.garden.id, bed.id))
        self.assertEqual(response.status_code, 200)
        form = {'parcel': self.parcel.id, 'name': 'ChangingName', 'length': '450', 'width': '350', 'exposition': 'NO', 'comment': 'nocomment',
                'soil_type': 'oily'}
        response = self.client.post('/{}/update_bed/{}'.format(self.garden.id, bed.id), data=form)
        self.assertRedirects(response, expected_url='/{}'.format(self.garden.id), status_code=302,
                             target_status_code=200)
        self.assertEqual(Bed.objects.get(pk=bed.id).name, 'ChangingName')

    def test_delete_bed(self):
        bed = Bed.objects.create(garden=self.garden, name='FirstBed', width=250, length=250)
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get('/{}/delete_bed/{}'.format(self.garden.id, bed.id))
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/{}/delete_bed/{}'.format(self.garden.id, bed.id))
        self.assertRedirects(response, expected_url='/{}'.format(self.garden.id), status_code=302,
                             target_status_code=200)
        self.assertEqual(len(Bed.objects.filter(pk=bed.id)), 0)
