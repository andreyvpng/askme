from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Answer, Like, Question

User = get_user_model()

admin.site.register(User)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Like)
