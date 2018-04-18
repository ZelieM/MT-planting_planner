from django.contrib.auth.models import User
from django.test import TestCase, Client

from planner.models import Garden


class AuthenticationViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = 'test_user'
        self.email = 'test@whatever.com'
        self.password = 'test'
        self.user = User.objects.create_user(self.username, self.email, self.password)

    def test_access_garden_selection_view(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get('/garden_selection')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['gardens_followed']), 0)
        self.assertFalse(response.context['is_searcher'])
        form = {'name': "NewGarden", 'postal_code': '4444'}
        response = self.client.post('/garden_selection', form)
        garden_created = Garden.objects.get(name="NewGarden")
        self.assertEqual(Garden.objects.get(name="NewGarden").postal_code, 4444)
        self.assertRedirects(response, expected_url='/{}/alerts'.format(garden_created.id), status_code=302, target_status_code=200)


    def test_login(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get('/logout')
        self.assertRedirects(response, '/login/', status_code=302)

    def test_signup(self):
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)
        form = {'username': 'user', 'password':'passwd','mailaddress': 'mymail@mail.com'}
        response = self.client.post('/signup', form)
        self.assertRedirects(response, expected_url='/garden_selection', status_code=302, target_status_code=200)

    def test_index(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/login', status_code=302,
                             target_status_code=301)  # /login permanently redirects to /login/
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get('/')
        self.assertRedirects(response, '/garden_selection', status_code=302, target_status_code=200)
