from django import forms
from django.forms import (
    CheckboxSelectMultiple,
    HiddenInput,
    RadioSelect
)

from quiz.models import (
    ChoiceQuizEntry,
    MultipleChoiceQuizEntry,
    ShortAnswerQuizEntry,
    TrueFalseQuizEntry
)


class ShortAnswerQuizEntryForm(forms.ModelForm):
    id = forms.IntegerField(max_value=4, min_value=0, widget=HiddenInput)

    class Meta:
        model = ShortAnswerQuizEntry
        fields = ['answer']


class TrueFalseQuizEntryForm(forms.ModelForm):
    id = forms.IntegerField(max_value=4, min_value=0, widget=HiddenInput)
    answer = forms.TypedChoiceField(
        coerce=lambda value: bool(int(value)),
        choices=((1, 'True'), (0, 'False')),
        widget=RadioSelect
    )

    class Meta:
        model = TrueFalseQuizEntry
        fields = ['answer']


def create_choice_form(choice_entry):
    class ChoiceQuizEntryForm(forms.ModelForm):
        ANSWER_CHOICES = [
            ('_'.join(choice.lower().split()), choice)
            for choice in choice_entry.answer_choices
        ]

        id = forms.IntegerField(max_value=4, min_value=0, widget=HiddenInput)
        answer = forms.ChoiceField(
            choices=ANSWER_CHOICES,
            widget=RadioSelect
        )

        class Meta:
            model = ChoiceQuizEntry
            fields = ['answer']

    return ChoiceQuizEntryForm


def create_multiple_choice_form(multiple_choice_entry):
    class MultipleChoiceQuizEntryForm(forms.ModelForm):
        ANSWER_CHOICES = [
            ('_'.join(choice.lower().split()), choice)
            for choice in multiple_choice_entry.answer_choices
        ]
        id = forms.IntegerField(max_value=4, min_value=0, widget=HiddenInput)
        answer = forms.MultipleChoiceField(
            choices=ANSWER_CHOICES,
            widget=CheckboxSelectMultiple
        )

        class Meta:
            model = MultipleChoiceQuizEntry
            fields = ['answer']

    return MultipleChoiceQuizEntryForm
