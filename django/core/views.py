from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls.base import reverse
from django.views.generic import CreateView, DetailView

from .forms import QuestionForm
from .models import Answer, Question


class AnswerDetailView(DetailView):
    queryset = Answer.objects.all_with_question()


class CreateQuestionView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.asked_by = self.request.user
        self.object.asked_to = self.get_user()
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'user:profile',
            kwargs={
                'pk': self.get_user().id
            }
        )

    def get_user(self):
        return User.objects.get(id=self.kwargs['pk'])
