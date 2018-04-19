from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase, Client

from planner.models import Garden, Vegetable, Bed, CultivatedArea, ForthcomingOperation, COWithDate, History


class AlertsViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = 'test_user'
        self.email = 'test@whatever.com'
        self.password = 'test'
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.garden = Garden.objects.create(name="MyGarden", postal_code=1000)
        History.objects.create(garden=self.garden)
        self.garden.users.add(self.user)
        self.vegetable = Vegetable.objects.create(name="Tomato", variety="Yellow Pearshaped", garden=self.garden)
        self.surface = Bed.objects.create(name="Bedding", garden=self.garden, width=250, length=250)
        operation = COWithDate.objects.create(name="Work", vegetable=self.vegetable, absoluteDate=date(2018, 8, 3))
        area = CultivatedArea.objects.create(vegetable=self.vegetable, garden=self.garden, label="Tomato area",
                                             surface=self.surface)
        self.alert = ForthcomingOperation.objects.create(area_concerned=area, original_cultural_operation=operation)

    def test_alert_view_index(self):
        response = self.client.get('/{}/alerts'.format(self.garden.id))
        self.assertRedirects(response, expected_url='/login/?next=/{}/alerts'.format(self.garden.id), status_code=302)
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/{}/alerts'.format(self.garden.id))
        self.assertEqual(response.status_code, 200)

    def test_add_seed(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/{}/alerts/add_seed'.format(self.garden.id))
        self.assertEqual(response.status_code, 200)
        form = {'vegetable_selection': self.vegetable.id, "seeding_label": "My seeding",
                "surface_selection": self.surface.id}
        self.assertEqual(len(CultivatedArea.objects.filter(label="My seeding")), 0)
        response = self.client.post('/{}/alerts/add_seed'.format(self.garden.id), form)
        self.assertRedirects(response, '/{}/alerts'.format(self.garden.id))
        self.assertEqual(len(CultivatedArea.objects.filter(label="My seeding")), 1)

    def test_validate_alert(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/{}/alerts/{}/validate'.format(self.garden.id, self.alert.id))
        self.assertEqual(response.status_code, 200)
        form = {'duration': "00:10:22", "execution_date": "2018-04-04",
                "validation_note": ""}
        response = self.client.post('/{}/alerts/{}/validate'.format(self.garden.id, self.alert.id), form)
        self.assertRedirects(response, '/{}/alerts'.format(self.garden.id))
        self.assertTrue(ForthcomingOperation.objects.get(pk=self.alert.id).is_done)
        self.assertEqual(ForthcomingOperation.objects.get(pk=self.alert.id).execution_date, date(2018, 4, 4))

    def test_postpone_alert(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/{}/alerts/{}/postpone'.format(self.garden.id, self.alert.id))
        self.assertEqual(response.status_code, 200)
        form = {'postponement_in_days': "5"}
        response = self.client.post('/{}/alerts/{}/postpone'.format(self.garden.id, self.alert.id), form)
        self.assertRedirects(response, '/{}/alerts'.format(self.garden.id))
        self.assertEqual(ForthcomingOperation.objects.get(pk=self.alert.id).postponement, 5)

    def test_delete_useless_alert(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/{}/alerts/{}/delete'.format(self.garden.id, self.alert.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.garden.history.historyitem_set.count(), 0)
        form = {'deletion_justification': "useless", "note": ""}
        response = self.client.post('/{}/alerts/{}/delete'.format(self.garden.id, self.alert.id), form)
        self.assertRedirects(response, '/{}/alerts'.format(self.garden.id))
        self.assertTrue(ForthcomingOperation.objects.get(pk=self.alert.id).is_done)
        self.assertEqual(self.garden.history.historyitem_set.count(), 1)

    def test_delete_destruction_alert(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/{}/alerts/{}/delete'.format(self.garden.id, self.alert.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.garden.history.historyitem_set.count(), 0)
        form = {'deletion_justification': "destruction", "note": ""}
        response = self.client.post('/{}/alerts/{}/delete'.format(self.garden.id, self.alert.id), form)
        self.assertRedirects(response, '/{}/alerts'.format(self.garden.id))
        self.assertTrue(ForthcomingOperation.objects.get(pk=self.alert.id).is_done)
        self.assertEqual(self.garden.history.historyitem_set.count(), 1)

    def test_print_forthcoming_operations(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/{}/alerts/print'.format(self.garden.id))
        self.assertEqual(response.status_code, 200)
        form = {'delay_to_print': "8"}
        response = self.client.post('/{}/alerts/print'.format(self.garden.id), form)
        self.assertEqual(response.status_code, 200)
