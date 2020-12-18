from django.contrib import admin

from quiz.models import (
    ChoiceQuizEntry,
    MultipleChoiceQuizEntry,
    ShortAnswerQuizEntry,
    TrueFalseQuizEntry
)


@admin.register(ChoiceQuizEntry)
class ChoiceQuizEntryAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'answer_choices')


@admin.register(MultipleChoiceQuizEntry)
class MultipleChoiceQuizEntryAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'answer_choices')


@admin.register(ShortAnswerQuizEntry)
class ShortAnswerQuizEntryAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')


@admin.register(TrueFalseQuizEntry)
class TrueFalseQuizEntryAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')
