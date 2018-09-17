from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField

User = get_user_model()


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['location', 'gender']


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}
