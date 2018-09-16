from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http.response import HttpResponseBadRequest
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views.generic import CreateView, DeleteView, DetailView

from .forms import AnswerForm, QuestionForm
from .models import Answer, Like, Question


class AnswerDetailView(DetailView):
    queryset = Answer.objects.all_with_question()


class AnswerCreateView(LoginRequiredMixin, CreateView):
    model = Answer
    form_class = AnswerForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.question = self.get_question()

        if self.object.question.asked_to != self.request.user:
            return HttpResponseBadRequest()

        self.object.save()

        return super().form_valid(form)

    def get_question(self):
        return Question.objects.get(id=self.kwargs['pk'])


class AnswerDeleteView(LoginRequiredMixin, DeleteView):
    model = Answer
    success_url = reverse_lazy('user:my-profile')

    def dispatch(self, *args, **kwargs):
        answer = self.get_object()

        if answer.question.asked_to != self.request.user:
            raise PermissionDenied

        return super().dispatch(*args, **kwargs)


class PrivateQuestionDetailView(DetailView):
    model = Question

    def dispatch(self, *args, **kwargs):
        question = self.get_object()

        if question.asked_to != self.request.user:
            raise PermissionDenied

        try:
            return reverse(question.answer.get_absolute_url())
        except ObjectDoesNotExist:
            pass

        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        answer_form = AnswerForm()
        ctx.update({'answer_form': answer_form})

        return ctx


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.asked_by = self.request.user
        self.object.asked_to = self.get_user()
        self.object.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('user:profile', kwargs={
            'pk': self.get_user().id
        })

    def get_user(self):
        return User.objects.get(id=self.kwargs['pk'])


class QuestionDeleteView(LoginRequiredMixin, DeleteView):
    model = Question
    success_url = reverse_lazy('user:inbox')

    def dispatch(self, *args, **kwargs):
        question = self.get_object()

        if question.asked_to != self.request.user:
            raise PermissionDenied

        return super().dispatch(*args, **kwargs)


class LikeCreateView(LoginRequiredMixin, CreateView):
    model = Like
    fields = []

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.liked_by = self.request.user
        self.object.answer = self.get_answer()

        self.object.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('core:answer-detail', kwargs={
            'pk': self.object.answer.id
        })

    def get_answer(self):
        return Answer.objects.get(id=self.kwargs['pk'])


class LikeDeleteView(LoginRequiredMixin, DeleteView):
    model = Like

    def dispatch(self, *args, **kwargs):
        like = self.get_object()

        if like.liked_by != self.request.user:
            raise PermissionDenied

        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('core:answer-detail', kwargs={
            'pk': self.get_answer().id
        })

    def get_answer(self):
        return Answer.objects.get(id=self.kwargs['pk'])
