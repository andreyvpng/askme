from user.factories import UserFactory

from django.test import TestCase


class UserModelTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory(username='testuser1', password='12345')
        self.other_user = UserFactory(username='testuser2', password='12345')

    def test_get_absolute_url(self):
        self.assertEquals(self.user.get_absolute_url(), '/user/1')
