from core.forms import QuestionForm
from core.models import Question
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, RedirectView

from .forms import RegisterForm

User = get_user_model()


class RegisterView(CreateView):
    template_name = 'user/register.html'
    form_class = RegisterForm

    def get_success_url(self):
        return reverse('user:login')


class UserListView(ListView):
    template_name = 'user/user_list.html'

    def get_queryset(self):
        qs = User.objects.order_by('username')
        return qs


class ProfileDetailView(DetailView):
    model = User
    template_name = 'user/profile.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        answered_questions = Question.objects.all_that_have_an_answer(
            self.object
        )

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
                'user:profile',
                kwargs={
                    'pk': self.request.user.id
                }
            )
        else:
            return reverse(
                settings.LOGIN_URL
            )


class InboxListView(LoginRequiredMixin, ListView):
    template_name = 'user/inbox.html'

    def get_queryset(self):
        qs = Question.objects.all_that_not_answered(
            self.request.user
        )
        return qs
