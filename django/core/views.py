from django.contrib.auth.models import User
from django.views.generic import DetailView

from .forms import QuestionForm
from .models import Question


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
