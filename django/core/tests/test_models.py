from user.factories import UserFactory
from core.factories import QuestionFactory, AnswerFactory
from core.models import Like

from django.test import TestCase


class AnswerModelTestCase(TestCase):

    LOREM_IPSUM = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus malesuada mi vitae mauris vulputate tincidunt."

    def setUp(self):
        self.user = UserFactory(username='testuser1', password='12345')
        self.other_user = UserFactory(username='testuser2', password='12345')
        self.question = QuestionFactory(
            asked_by=self.other_user,
            asked_to=self.user,
            text=self.LOREM_IPSUM
        )
        self.answer = AnswerFactory(
            question=self.question
        )

    def test_get_absolute_url(self):
        self.assertEquals(
            self.answer.get_absolute_url(),
            '/answer/{}'.format(self.answer.id)
        )

    def test_total_likes(self):
        self.assertEquals(self.answer.total_likes(), 0)
        Like.objects.create(
            liked_by=self.other_user,
            answer=self.answer,
        )
        self.assertEquals(self.answer.total_likes(), 1)
        Like.objects.create(
            liked_by=self.user,
            answer=self.answer,
        )
        self.assertEquals(self.answer.total_likes(), 2)
