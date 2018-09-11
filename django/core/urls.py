from django.urls import path

from . import views

app_name = 'core'
urlpatterns = [
    path('answer/<int:pk>',
         views.AnswerDetailView.as_view(), name='answer-detail'),
    path('ask/<int:pk>',
         views.CreateQuestionView.as_view(), name='ask'),
]
