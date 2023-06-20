from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from . import models


class AnswerInline(admin.TabularInline):
    model = models.Answer


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


class QuizAdmin(admin.ModelAdmin):
    model = models.Quiz
    list_display = ('name', 'topic', 'number_of_questions')
    list_filter = ('topic', )
    search_fields = ('name', )


class ResultAdmin(admin.ModelAdmin):
    model = models.Result
    list_display = ('quiz', 'user', 'score')


admin.site.register(models.Quiz, QuizAdmin)
admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Answer)
admin.site.register(models.Result, ResultAdmin)
