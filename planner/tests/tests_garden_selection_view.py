from django.contrib.auth.models import User
from django.test import TestCase, Client


class GardenSelectionViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = 'test_user'
        self.email = 'test@whatever.com'
        self.password = 'test'
        self.user = User.objects.create_user(self.username, self.email, self.password)

    def test_access_garden_selection_view(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/garden_selection')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['gardens_followed']),0)
        self.assertFalse(response.context['is_searcher'])
