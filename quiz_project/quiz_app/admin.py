from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from . import models


class AnswerInline(admin.TabularInline):
    model = models.Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


admin.site.register(models.Quiz)
admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Answer)
admin.site.register(models.Result)
