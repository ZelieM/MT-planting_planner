from django.contrib.auth.models import User
from django.test import TestCase, Client

from planner.models import Garden, Bed, Vegetable, CultivatedArea


class CropsManagementViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = 'test_user'
        self.email = 'test@whatever.com'
        self.password = 'test'
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.garden = Garden.objects.create(name="MyGarden", postal_code=1000)
        self.garden.users.add(self.user)

    def test_index_view(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get('/{}/crops'.format(self.garden.id))
        self.assertEqual(response.status_code, 200)

    def test_delete_crop(self):
        surface = Bed.objects.create(garden=self.garden, name="Bed", width=250, length=250)
        vegetable = Vegetable.objects.create(name="Veggie", variety="Eatable", garden=self.garden)
        area = CultivatedArea.objects.create(label="VeggieArea", vegetable=vegetable, surface=surface, garden=self.garden)
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get('/{}/{}/terminate_cropping'.format(self.garden.id, area.id))
        self.assertEqual(response.status_code, 200)
        form = {'harvest_date': '2018-04-18'}
        response = self.client.post('/{}/{}/terminate_cropping'.format(self.garden.id, area.id), form)
        self.assertRedirects(response, expected_url='/{}/crops'.format(self.garden.id), status_code=302, target_status_code=200)
        self.assertFalse(CultivatedArea.objects.get(pk=area.id).is_active)