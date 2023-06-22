from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from . import models


def index(request):
    num_quizes = models.Quiz.objects.all().count()
  
    context = {
        'num_quizes': num_quizes,
    }

    return render(request, 'library/index.html', context)


def quiz_list(request):
    quizzes = models.Quiz.objects.all()
    return render(request, 'library/quiz_list.html', {
        'quizzes': quizzes
        })

def quiz_details(request, pk: int):
    quiz = get_object_or_404(models.Quiz, pk=pk)
    if request.method == 'POST':
        questions = quiz.get_questions()
        score = 0
        attempted_questions = []  # Store the attempted questions
        user_answers = []
        user_incorrect_answers = []

        for question in questions:
            selected_answer_id = request.POST.get('question{}'.format(question.id))
            selected_answer = question.answers.filter(id=selected_answer_id).first()
            if selected_answer and selected_answer.correct:
                score += 1
                attempted_questions.append(question)  # Add the attempted question
                user_answers.append(selected_answer)  # Add the user's answer
            elif selected_answer == False:  # Answered incorrectly
                attempted_questions.append(question)
            else:
                user_incorrect_answers.append(selected_answer)
        result = models.Result.objects.create(
            quiz=quiz,
            user=request.user,
            score=round((score/quiz.number_of_questions*100),2)
        )
        result.questions_attempted.set(attempted_questions)
        result.user_answers.set(user_answers)
        result.user_incorrect_answers.set(user_incorrect_answers)
        return HttpResponseRedirect(reverse('quiz_app:result_detail', args=[result.pk]))
    else:
        questions = quiz.get_questions()
        return render(request, 'library/quiz_form.html', {
            'quiz': quiz,
            'questions': questions
        })


class ResultDetailView(LoginRequiredMixin, DetailView):
    model = models.Result
    template_name = 'library/result_detail.html'
