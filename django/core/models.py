from django.contrib.auth.models import User
from django.db import models


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


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

    def __str__(self):
        return self.text[:75]


class Answer(TimeStampedModel):
    text = models.TextField(default=None)
    question = models.OneToOneField(Question,
                                    related_name='answer',
                                    on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:75]
