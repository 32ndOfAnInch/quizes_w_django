from django.db import models
# from django.contrib.auth.models import User    # not the best way
from django.utils.translation import gettext_lazy as _
import random
from django.contrib.auth import get_user_model
from django.urls import reverse
from tinymce.models import HTMLField

User = get_user_model()


class Topic(models.Model):
    name = models.CharField(_("name"), max_length=100)

    class Meta:
        verbose_name = _("topic")
        verbose_name_plural = _("topics")

    def __str__(self):
        return f"{self.name}"


class Quiz(models.Model):
    name = models.CharField(_("name"), max_length=120)
    topic = models.ManyToManyField(
        Topic,
        verbose_name=_("topic"), 
        help_text=_("choose topic(s) for this quiz")
        )
    number_of_questions = models.IntegerField(_("number of questions"))
    date_created = models.DateTimeField(_("quiz_submit_date"), auto_now_add=True)
    score_to_pass = models.IntegerField(_("required score to pass"), help_text="required score in %")

    def __str__(self):
        return f"{self.name}-{self.topic}"

    def get_questions(self):
        questions = list(self.questions.all())
        random.shuffle(questions)
        return questions[:self.number_of_questions]
    

    class Meta:
        ordering = ['name', 'date_created']
        verbose_name = _("quiz")
        verbose_name_plural = _("quizes")

    def __str__(self):
        return f"{self.name} {self.topic} {self.number_of_questions}"

    def get_absolute_url(self):
        return reverse("quiz_detail", kwargs={"pk": self.pk})
    
    def display_topic(self):
        return ', '.join(topic.name for topic in self.topic.all()[:3])
    display_topic.short_description = _('topic')


class Question(models.Model):
    text = HTMLField(_("text"), max_length=3000)
    quiz = models.ForeignKey(
        Quiz,
        verbose_name=_("quiz"),
        on_delete=models.CASCADE,
        related_name='questions',
        )


    class Meta:
        verbose_name = _("question")
        verbose_name_plural = _("questions")

    def __str__(self):
        return f"{self.text}"

    def get_answers(self):
        return self.answers.all()
    
    def get_absolute_url(self):
        return reverse("question_detail", kwargs={"pk": self.pk})


class Answer(models.Model):
    text = models.CharField(_("text"), max_length=200)
    correct = models.BooleanField(_("correct"), default=False)
    question = models.ForeignKey(
        Question,
        verbose_name=_("question"),
        on_delete=models.CASCADE,
        related_name="answers",
        )


    class Meta:
        verbose_name = _("answer")
        verbose_name_plural = _("answers")

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.text}, correct: {self.correct}"
    
    def get_absolute_url(self):
        return reverse("answer_detail", kwargs={"pk": self.pk})
    

class Result(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        verbose_name=_("result"),
        on_delete=models.CASCADE,
        related_name="results",
    )
    user = models.ForeignKey(
        User,
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        related_name="quiz_results",
    )
    score = models.FloatField(_("score"))
    questions_attempted = models.ManyToManyField(Question, related_name="result_attempts")
    user_answers = models.ManyToManyField(
        Answer,
        verbose_name=_("user answers"),
        blank=True,
        related_name="user_results",
    )

    user_incorrect_answers = models.ManyToManyField(
        Answer,
        verbose_name=_("user incorrect answers"),
        blank=True,
        related_name="user_incorrect_results",
    )

    submit_date = models.DateTimeField(_("quiz_submit_date"), auto_now_add=True)

    class Meta:
        verbose_name = _("result")
        verbose_name_plural = _("results")

    def __str__(self):
        return f"{self.pk}"
    
    def get_absolute_url(self):
        return reverse("result_detail", kwargs={"pk": self.pk})