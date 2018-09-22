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


class UserListViewTest(TestCase):
    USER_LIST_HTML = """
      <li class="media mb-2">
        <img class='mr-3' src="{image}" alt="">
        <div class="media-body">
          <a href="{url}">
            <h5 class="mt-0 mb-1">{name}</h5>
          </a>
        </div>
      </li>
    """

    def setUp(self):
        self.user = UserFactory(username='testuser1', password='12345')
        self.other_user = UserFactory(username='testuser2', password='12345')

    def test_list_of_users_tempalate(self):
        resp = self.client.get('/user/')
        rendered_content = resp.rendered_content

        FULL_LIST_OF_USERS = ''
        users = resp.context_data['object_list']

        for user in users:
            FULL_LIST_OF_USERS += self.USER_LIST_HTML.format(
                image=user.avatar_url,
                url=user.get_absolute_url(),
                name=user.username
            )

        self.assertInHTML(FULL_LIST_OF_USERS, rendered_content)
