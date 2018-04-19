from django.contrib.auth.models import User, Permission
from django.test import TestCase, Client


class GardensDataViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = 'test_user'
        self.email = 'test@whatever.com'
        self.password = 'test'
        self.user = User.objects.create_user(self.username, self.email, self.password)

    def test_index(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get('/research/')
        self.assertRedirects(response, '/login/?next=/research/')
        permission = Permission.objects.get(name='Can access research interface')
        self.user.user_permissions.add(permission)
        response = self.client.get('/research/')
        self.assertEqual(response.status_code, 200)
