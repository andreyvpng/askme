from user.factories import UserFactory

import factory

from .models import Answer, Question


class CreateFactoryMixin(factory.DjangoModelFactory):

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create(*args, **kwargs)


class QuestionFactory(CreateFactoryMixin, factory.DjangoModelFactory):
    text = factory.Sequence(lambda n: 'Question #%d' % n)
    asked_to = factory.SubFactory(UserFactory)
    asked_by = factory.SubFactory(UserFactory)

    class Meta:
        model = Question


class AnswerFactory(CreateFactoryMixin, factory.DjangoModelFactory):
    text = factory.Sequence(lambda n: 'Answer #%d' % n)
    question = factory.SubFactory(QuestionFactory)

    class Meta:
        model = Answer
