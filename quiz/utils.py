import random

from quiz.forms import (
    create_choice_form,
    create_multiple_choice_form,
    ShortAnswerQuizEntryForm,
    TrueFalseQuizEntryForm
)
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

    for id_, entry in enumerate(random_entries):
        entry.id_ = id_
        entry.type = entry.__class__.__name__

    return random_entries


def get_total_quiz_entries():
    return (
        ChoiceQuizEntry.objects.count()
        + MultipleChoiceQuizEntry.objects.count()
        + ShortAnswerQuizEntry.objects.count()
        + TrueFalseQuizEntry.objects.count()
    )


def get_quiz_entry_form(entry):
    if isinstance(entry, ChoiceQuizEntry):
        return create_choice_form(entry)

    elif isinstance(entry, MultipleChoiceQuizEntry):
        return create_multiple_choice_form(entry)

    elif isinstance(entry, ShortAnswerQuizEntry):
        return ShortAnswerQuizEntryForm

    elif isinstance(entry, TrueFalseQuizEntry):
        return TrueFalseQuizEntryForm


def get_quiz_entry_model(entry_name, pk):
    if entry_name == 'ChoiceQuizEntry':
        return ChoiceQuizEntry.objects.get(pk=pk)

    elif entry_name == 'MultipleChoiceQuizEntry':
        return MultipleChoiceQuizEntry.objects.get(pk=pk)

    elif entry_name == 'ShortAnswerQuizEntry':
        return ShortAnswerQuizEntry.objects.get(pk=pk)

    elif entry_name == 'TrueFalseQuizEntry':
        return TrueFalseQuizEntry.objects.get(pk=pk)


def validate_entry_submission(entry, request):
    model = get_quiz_entry_model(entry['type'], entry['pk'])
    form = get_quiz_entry_form(model)
    answer = dict(request.POST).get('answer')

    if not answer:
        return False

    if entry['type'] == 'MultipleChoiceQuizEntry':
        answer_choices = dict(form.ANSWER_CHOICES)
        answer = [answer_choices[a] for a in answer]

        return set(answer) == set(model.answer.split(','))

    if entry['type'] == 'ChoiceQuizEntry':
        answer = dict(form.ANSWER_CHOICES)[answer[0]]

        return answer == model.answer[0]

    elif entry['type'] == 'TrueFalseQuizEntry':
        return int(answer[0]) == model.answer

    else:
        return answer[0] == model.answer
