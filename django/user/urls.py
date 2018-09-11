from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    path('login',
         LoginView.as_view(), name='login'),
    path('logout',
         LogoutView.as_view(), name='logout'),
    path('register',
         views.RegisterView.as_view(), name='register'),
    path('',
         views.MyProfileView.as_view(), name='my-profile'),
    path('<int:pk>/',
         views.ProfileDetailView.as_view(), name='profile'),
    path('inbox',
         views.InboxListView.as_view(), name='inbox')
]
