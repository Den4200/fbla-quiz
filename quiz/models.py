from django.contrib.postgres.fields import ArrayField
from django.db import models


class QuizEntry(models.Model):
    question = models.CharField(
        max_length=4096,
        help_text='The question of the entry.'
    )

    answer: models.Field

    class Meta:
        abstract = True


class ChoiceQuizEntry(QuizEntry):
    answer = ArrayField(
        models.CharField(max_length=256),
        help_text='The answers to the question.'
    )

    answer_choices = ArrayField(
        models.CharField(max_length=256),
        help_text='All possible choices for a question, including the answers themselves.'
    )


class MultipleChoiceQuizEntry(QuizEntry):
    answer = models.CharField(
        max_length=256,
        help_text='The answer to the question.'
    )

    answer_choices = ArrayField(
        models.CharField(max_length=256),
        help_text='All possible choices for a question, including the answer itself.'
    )


class ShortAnswerQuizEntry(QuizEntry):
    answer = models.CharField(
        max_length=256,
        help_text='The answer to the question.'
    )


class TrueFalseQuizEntry(QuizEntry):
    answer = models.BooleanField(help_text='The answer to the question.')
