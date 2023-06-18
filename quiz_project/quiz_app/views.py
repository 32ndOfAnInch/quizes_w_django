from django.shortcuts import render
from . import models


def index(request):
    num_quizes = models.Quiz.objects.all().count()
  
    context = {
        'num_quizes': num_quizes,
    }

    return render(request, 'library/index.html', context)
