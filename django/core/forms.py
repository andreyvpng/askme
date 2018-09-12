from django import forms

from .models import Answer, Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'anonymous']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
