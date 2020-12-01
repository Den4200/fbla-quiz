import random

from quiz.models import (
    ChoiceQuizEntry,
    MultipleChoiceQuizEntry,
    ShortAnswerQuizEntry,
    TrueFalseQuizEntry
)


def get_random_quiz_entries(amount):
    entries = [
        *ChoiceQuizEntry.objects.all(),
        *MultipleChoiceQuizEntry.objects.all(),
        *ShortAnswerQuizEntry.objects.all(),
        *TrueFalseQuizEntry.objects.all(),
    ]

    random_entries = random.sample(entries, amount)

    for entry in random_entries:
        entry.type = entry.__class__.__name__

    return random_entries


def get_total_quiz_entries():
    return (
        ChoiceQuizEntry.objects.count()
        + MultipleChoiceQuizEntry.objects.count()
        + ShortAnswerQuizEntry.objects.count()
        + TrueFalseQuizEntry.objects.count()
    )
