from django.urls import path

from quiz.views import IndexView, QuizView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('quiz/', QuizView.as_view(), name='quiz'),
]
