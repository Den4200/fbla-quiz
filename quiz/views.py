from django.shortcuts import render
from django.views import View

from quiz.utils import get_total_quiz_entries


class IndexView(View):
    template_name = 'quiz/index.html'

    def get(self, request):
        entry_count = get_total_quiz_entries()
        return render(request, self.template_name, {'entry_count': entry_count})
