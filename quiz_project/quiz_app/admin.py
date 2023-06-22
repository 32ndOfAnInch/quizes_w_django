from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from . import models


class AnswerInline(admin.TabularInline):
    model = models.Answer


class QuestionAdmin(admin.ModelAdmin):
    model = models.Question
    list_display = ('text', 'quiz')
    search_fields = ('text', )
    inlines = [AnswerInline]


class QuizAdmin(admin.ModelAdmin):
    model = models.Quiz
    list_display = ('name',  'number_of_questions', 'score_to_pass', 'date_created', 'display_topic',)
    list_filter = ('topic', )
    search_fields = ('name', )


class ResultAdmin(admin.ModelAdmin):
    model = models.Result
    list_display = ('quiz', 'user', 'score')


class TopicAdmin(admin.ModelAdmin):
    model = models.Topic
    list_display = ('name', )

admin.site.register(models.Topic, TopicAdmin)
admin.site.register(models.Quiz, QuizAdmin)
admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Answer)
admin.site.register(models.Result, ResultAdmin)
