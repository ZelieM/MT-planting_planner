from datetime import date

from django.contrib.auth.models import User, Permission
from django.test import TestCase, Client


class GardensDataViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = 'test_user'
        self.email = 'test@whatever.com'
        self.password = 'test'
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.permission = Permission.objects.get(name='Can access research interface')

    def test_index(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get('/research/')
        self.assertRedirects(response, '/login/?next=/research/')
        self.user.user_permissions.add(self.permission)
        response = self.client.get('/research/')
        self.assertEqual(response.status_code, 200)

    def test_export_data(self):
        self.user.user_permissions.add(self.permission)
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/research/export_gardens')
        filename = "gardens_data_{}.csv".format(str(date.today()))
        self.assertEquals(
            response.get('Content-Disposition'),
            "attachment; filename={}".format(filename)
        )