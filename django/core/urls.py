from django.urls import path

from . import views

app_name = 'core'
urlpatterns = [
    path('u/<int:pk>/',
         views.ProfileDetailView.as_view(), name='profile'),
    path('u/<int:pk>/ask/',
         views.CreateQuestionView.as_view(), name='ask'),
    path('',
         views.MyProfileView.as_view(), name='my_profile')
]
