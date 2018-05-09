from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase, Client

from planner.models import Garden, Vegetable, COWithDate, COWithOffset

OP_DATE = date(2018, 3, 15)


class CulturalOperationsViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = 'JohnSmith'
        self.email = 'john@smith.com'
        self.password = 'johnsmith'
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.garden = Garden.objects.create(name="MyGarden", postal_code=1000)
        self.garden.users.add(self.user)
        self.vegetable = Vegetable.objects.create(garden=self.garden, name="Pumpkin", variety="Red kuri")

    def test_cowithdate(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/{}/{}/add_date_co'.format(self.garden.id, self.vegetable.id))
        self.assertEqual(response.status_code, 200)
        form = {'name': 'FirstOperation', 'vegetable': self.vegetable.id, 'absoluteDate': str(OP_DATE),
                'duration': '00:10:10'}
        response = self.client.post('/{}/{}/add_date_co'.format(self.garden.id, self.vegetable.id), form)
        self.assertRedirects(response, '/{}/vegetables'.format(self.garden.id))
        self.assertEqual(self.vegetable.culturaloperation_set.count(), 1)

    def test_cowidhtoffset(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/{}/{}/add_offset_co'.format(self.garden.id, self.vegetable.id))
        self.assertEqual(response.status_code, 200)
        previousop = COWithDate.objects.create(name="FirstOp", vegetable=self.vegetable, absoluteDate=OP_DATE)
        form = {'name': "Offset_op", 'vegetable': self.vegetable.id, 'previous_operation': previousop.id,
                'offset_in_days': "5", 'duration': "00:10:10"}
        response = self.client.post('/{}/{}/add_offset_co'.format(self.garden.id, self.vegetable.id), form)
        self.assertRedirects(response, '/{}/vegetables'.format(self.garden.id))
        self.assertEqual(self.vegetable.culturaloperation_set.count(), 2)
        self.assertTrue(COWithOffset.objects.get(name="Offset_op").vegetable_id, self.vegetable.id)

    def test_delete_op(self):
        self.client.login(username=self.username, password=self.password)
        op = COWithDate.objects.create(name="FirstOp", vegetable=self.vegetable, absoluteDate=OP_DATE)
        response = self.client.get('/{}/vegetables/delete_co/{}'.format(self.garden.id, op.id))
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(COWithDate.DoesNotExist):
            COWithDate.objects.get(name="FirstOp")
