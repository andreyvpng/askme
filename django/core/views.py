from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.urls.base import reverse
from django.views.generic import CreateView, DetailView

from .forms import AnswerForm, QuestionForm
from .models import Answer, Question


class AnswerDetailView(DetailView):
    queryset = Answer.objects.all_with_question()


class AnswerCreateView(CreateView):
    model = Answer
    form_class = AnswerForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.question = self.get_question()
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'core:answer-detail',
            kwargs={
                'pk': self.object.id
            }
        )

    def get_question(self):
        return Question.objects.get(id=self.kwargs['pk'])


class PrivateQuestionDetailView(DetailView):
    model = Question

    def dispatch(self, *args, **kwargs):
        question = self.get_object()

        if question.asked_to != self.request.user:
            raise PermissionDenied

        try:
            return reverse('answer-detail', question.answer.id)
        except ObjectDoesNotExist:
            pass

        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        answer_form = AnswerForm()

        ctx.update({'answer_form': answer_form})

        return ctx


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
