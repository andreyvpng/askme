from django.contrib.auth.models import User
from django.db import models
from django.urls.base import reverse


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class QuestionManager(models.Manager):

    def all_with_answer(self):
        qs = self.get_queryset()
        qs = qs.select_related('answer')
        return qs

    def all_that_have_an_answer(self, user):
        qs = self.all_with_answer()
        qs = qs.filter(asked_to=user)
        qs = qs.exclude(answer=None)
        qs = qs.order_by('-created')
        return qs

    def all_that_not_answered(self, user):
        qs = self.all_with_answer()
        qs = qs.filter(asked_to=user, answer__exact=None)
        qs = qs.order_by('-created')
        return qs


class Question(TimeStampedModel):
    text = models.TextField(default=None)
    asked_to = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 related_name='asked_to_questions')
    asked_by = models.ForeignKey(User,
                                 default=None,
                                 null=True,
                                 on_delete=models.CASCADE,
                                 related_name='asked_by_questions')
    anonymous = models.BooleanField(default=True)
    objects = QuestionManager()

    def __str__(self):
        return self.text[:75]


class AnswerManager(models.Manager):

    def all_with_question(self):
        qs = self.get_queryset()
        qs = qs.select_related('question')
        return qs


class Answer(TimeStampedModel):
    text = models.TextField(default=None)
    question = models.OneToOneField(Question,
                                    related_name='answer',
                                    on_delete=models.CASCADE)
    objects = AnswerManager()

    def __str__(self):
        return self.text[:75]

    def get_absolute_url(self):
        return reverse('core:answer-detail', kwargs={
            'pk': self.id
        })
