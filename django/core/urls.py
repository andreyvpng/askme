from django.urls import path

from . import views

app_name = 'core'
urlpatterns = [
    path('answer/<int:pk>',
         views.AnswerDetailView.as_view(),
         name='answer-detail'),
    path('ask/<int:pk>',
         views.CreateQuestionView.as_view(),
         name='ask'),
    path('private-question/<int:pk>',
         views.PrivateQuestionDetailView.as_view(),
         name='private-question'),
    path('private-question/<int:pk>/create',
         views.AnswerCreateView.as_view(),
         name='answer-create'),
    path('answer/<int:pk>/delete',
         views.AnswerDeleteView.as_view(),
         name='answer-delete')
]
