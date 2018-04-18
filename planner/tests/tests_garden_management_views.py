from django.contrib.auth.models import User
from django.test import TestCase, Client

from planner.models import Garden, Bed


class GardenManagementViewsTests(TestCase):

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
        response = self.client.get('/{}/settings'.format(self.garden.id))
        self.assertEqual(response.status_code, 200)

    def test_update_garden_details(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get('/{}/settings/edit_details'.format(self.garden.id))
        self.assertEqual(response.status_code, 200)
        form = {'name': "NiceGarden", 'comment': "", 'soil_type': "", 'culture_type': "",
                'reference_email': 'reference@ref.be', 'details_available_for_research': 'on',
                'activity_data_available_for_research': 'on'}
        response = self.client.post('/{}/settings/edit_details'.format(self.garden.id), form)
        self.assertRedirects(response, '/{}/settings'.format(self.garden.id))
        self.assertEqual(Garden.objects.get(pk=self.garden.id).name, 'NiceGarden')

    def test_user_update_email(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get('/{}/settings/edit_email'.format(self.garden.id))
        self.assertEqual(response.status_code, 200)
        form = {'email': "hello@world.com"}
        response = self.client.post('/{}/settings/edit_email'.format(self.garden.id), form)
        self.assertRedirects(response, '/{}/settings'.format(self.garden.id))
        self.assertEqual(User.objects.get(pk=self.user.id).email, 'hello@world.com')

    def test_update_notification_delay(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get('/{}/settings/notification_delay'.format(self.garden.id))
        self.assertEqual(response.status_code, 200)
        # Test update of notification
        self.assertEqual(self.garden.notification_delay, 5)
        form = {'notification_delay': "45"}
        response = self.client.post('/{}/settings/notification_delay'.format(self.garden.id), form)
        self.assertRedirects(response, '/{}/settings'.format(self.garden.id))
        self.assertEqual(Garden.objects.get(pk=self.garden.id).notification_delay, 45)

    def test_add_user_to_garden(self):
        new_user = User.objects.create_user('JSmith', 'john@smith.com', 'supersecret')
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get('/{}/settings/add_user'.format(self.garden.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.garden.users.all()), 1)
        form = {'user_selection': new_user.id}
        response = self.client.post('/{}/settings/add_user'.format(self.garden.id), form)
        self.assertRedirects(response, '/{}/settings'.format(self.garden.id))
        self.assertEqual(len(self.garden.users.all()), 2)

    def test_delete_user(self):
        login = self.client.login(username=self.username, password=self.password)
        new_user = User.objects.create_user('JSmith', 'john@smith.com', 'supersecret')
        self.garden.users.add(new_user)
        delete_url = '/{}/settings/delete/{}'.format(self.garden.id, new_user.id)
        self.assertEqual(len(self.garden.users.all()), 2)
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(self.garden.users.all()), 1)
