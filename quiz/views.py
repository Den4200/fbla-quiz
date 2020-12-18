from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from quiz.utils import (
    get_random_quiz_entries,
    get_total_quiz_entries,
    get_quiz_entry_form,
    validate_entry_submission
)


class IndexView(View):
    template_name = 'quiz/index.html'

    def get(self, request):
        entry_count = get_total_quiz_entries()
        return render(request, self.template_name, {'entry_count': entry_count})


class QuizView(View):
    template_name = 'quiz/quiz.html'

    def get(self, request):
        entries = get_random_quiz_entries(5)
        request.session['entries'] = [
            {
                'id': entry.id_,
                'pk': entry.pk,
                'type': entry.type
            } for entry in entries
        ]
        context = [(entry, get_quiz_entry_form(entry)()) for entry in entries]

        return render(request, self.template_name, {'entries': context})

    def post(self, request):
        for idx, entry in enumerate(request.session['entries']):
            if entry['id'] == int(request.POST['entry_id'][0]):
                if validate_entry_submission(entry, request):
                    messages.success(
                        request,
                        'Correct answer!',
                        extra_tags=str(entry["id"])
                    )
                else:
                    messages.error(
                        request,
                        'Incorrect answer.',
                        extra_tags=f'{entry["id"]} danger'
                    )

                msgs = [
                    {
                        'level': message.level,
                        'message': message.message,
                        'tags': message.tags
                    }
                    for message in messages.get_messages(request)
                ]

                return JsonResponse({'messages': msgs})

        return redirect('index')
