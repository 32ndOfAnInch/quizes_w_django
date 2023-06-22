from django.urls import path
from . import views

app_name = 'quiz_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('quizzes/', views.QuizListView.as_view(), name='quiz_list'),
    path('quiz/<int:pk>/', views.quiz_details, name='quiz_details'),
    path('result/<int:pk>/', views.ResultDetailView.as_view(), name='result_detail'),
]
