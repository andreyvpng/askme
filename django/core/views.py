from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views.generic import CreateView, DeleteView, DetailView, View

from .forms import AnswerForm, QuestionForm
from .models import Answer, Like, Question

User = get_user_model()


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


class LikeView(LoginRequiredMixin, View):

    def post(self, request, pk):

        answer = Answer.objects.get(id=pk)
        like = Like.objects.filter(answer=answer,
                                   liked_by=request.user)

        if like:
            like.delete()
        else:
            like = Like.objects.create(answer=answer,
                                       liked_by=request.user)
            like.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
