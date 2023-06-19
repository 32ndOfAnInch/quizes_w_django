from django.shortcuts import render
from . import models
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse


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
        for question in questions:
            selected_answer_id = request.POST.get('question{}'.format(question.id))
            selected_answer = question.answers.filter(id=selected_answer_id).first()
            if selected_answer and selected_answer.correct:
                score += 1
        result = models.Result.objects.create(
            quiz=quiz,
            user=request.user,
            score=score/quiz.number_of_questions*100
        )
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