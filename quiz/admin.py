from django.contrib import admin

from quiz.models import (
    ChoiceQuizEntry,
    MultipleChoiceQuizEntry,
    ShortAnswerQuizEntry,
    TrueFalseQuizEntry
)


admin.site.register(ChoiceQuizEntry)
admin.site.register(MultipleChoiceQuizEntry)
admin.site.register(ShortAnswerQuizEntry)
admin.site.register(TrueFalseQuizEntry)
