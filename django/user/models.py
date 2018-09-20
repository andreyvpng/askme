from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    location = models.CharField(max_length=100, null=True)

    NOT_CHOSEN = 'N'
    MALE = 'M'
    FEMALE = 'F'
    GENDERS = (
        (NOT_CHOSEN, 'Not Chosen'),
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDERS,
        default=NOT_CHOSEN,
    )

    avatar_url = models.URLField(null=True)
    bio = models.CharField(max_length=200, null=True)

    def get_absolute_url(self):
        return reverse('user:profile', kwargs={
            'pk': self.id
        })
