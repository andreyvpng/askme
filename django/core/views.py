from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls.base import reverse
from django.views.generic import CreateView, DetailView, RedirectView

from .forms import QuestionForm
from .models import Answer, Question


class AnswerDetailView(DetailView):
    model = Answer


class CreateQuestionView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.asked_by = self.request.user
        self.object.asked_to = self.get_user()
        self.object.save()
        return super(CreateQuestionView, self).form_valid(form)

    def get_success_url(self):
        return reverse(
            'core:profile',
            kwargs={
                'pk': self.get_user().id
            }
        )

    def get_user(self):
        return User.objects.get(id=self.kwargs['pk'])


class ProfileDetailView(DetailView):
    model = User
    template_name = 'core/profile.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        answered_questions = Question.objects.exclude(answer=None).filter(
            asked_to=self.object).select_related('answer').order_by('-created')

        ctx.update({'questions': answered_questions})

        question_form = QuestionForm(initial={
            'creator': self.request.user.id,
            'user': self.object.id
        })

        ctx.update({'question_form': question_form})

        return ctx


class MyProfileView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return reverse(
                'core:profile',
                kwargs={
                    'pk': self.request.user.id
                }
            )
        else:
            return reverse(
                settings.LOGIN_URL
            )
