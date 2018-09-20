from user.factories import UserFactory

from django.test import TestCase


class MyProfileViewTest(TestCase):

    def setUp(self):
        self.user = UserFactory(username='testuser1', password='12345')
        self.other_user = UserFactory(username='testuser2', password='12345')

    def test_not_authorized_user(self):
        resp = self.client.get('/user/me')
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/user/login')

    def test_authorized_user(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get('/user/me')
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/user/{0}'.format(self.user.id))


class UserUpdateViewTest(TestCase):

    def setUp(self):
        self.user = UserFactory(username='testuser1', password='12345')
        self.other_user = UserFactory(username='testuser2', password='12345')

    def test_check_permission(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get('/user/{}/update'.format(self.user.id))
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/user/{}/update'.format(self.other_user.id))
        self.assertEqual(resp.status_code, 403)
