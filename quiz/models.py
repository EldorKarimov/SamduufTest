from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from common.models import BaseModel
from django.urls import reverse
import random
from datetime import datetime

User = get_user_model()

class Science(BaseModel):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, verbose_name=_("name"))

    def __str__(self):
        return self.name

class Test(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True, verbose_name="description")
    science = models.ForeignKey(Science, on_delete=models.CASCADE)
    duration = models.IntegerField(help_text="Testning davomiyligi daqiqalarda", verbose_name=_("duration"))
    attempts_allowed = models.IntegerField(help_text="Testni necha marta yechishga ruxsat beriladi", verbose_name=_("attemps allowed"))
    image = models.ImageField(upload_to='media/test/images', verbose_name=_("image"))
    number_of_questions = models.IntegerField(default=1, verbose_name=_("number of questions"))
    is_available = models.BooleanField(default=False)
    start_time = models.DateTimeField(verbose_name=_("start time"))
    end_time = models.DateTimeField(verbose_name=_("end time"))

    def __str__(self):
        return self.title
    
    def get_url(self, *args, **kwargs):
        return reverse('quiz:test_detail', kwargs={'test_id':self.id})
    
    @property
    def get_questions(self):
        questions = Question.objects.filter(test = self, is_available = True)
        questions = list(questions)
        try:
            questions = random.sample(questions, self.number_of_questions)
            return questions
        except Exception as e:
            return None
        

class Question(BaseModel):
    test = models.ForeignKey(Test, related_name="questions", on_delete=models.CASCADE, verbose_name=_("test"))
    name = models.TextField(verbose_name=_("name"))
    mark = models.IntegerField(default=1, verbose_name=_("mark"))
    is_multiple_choice = models.BooleanField(default=False, verbose_name=_("is multiple choice"))
    is_available = models.BooleanField(default=True, verbose_name=_("is available"))

    def __str__(self):
        return self.name
    
    @property
    def get_answers(self):
        answers = Answer.objects.filter(question = self)
        answers = list(answers)
        random.shuffle(answers)
        return answers

class Answer(BaseModel):
    question = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE, verbose_name=_("question"))
    name = models.CharField(max_length=255, verbose_name=_("name"))
    is_correct = models.BooleanField(default=False, verbose_name=_("is correct"))

    def __str__(self):
        return self.name

class UserAttempt(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("user"))
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name=_("test"))
    score = models.IntegerField(_("score"))
    time_taken = models.DurationField(_("time taken"))
    date_taken = models.DateTimeField(auto_now_add=True, verbose_name=_("date taken"))
    is_started = models.BooleanField(default=False, verbose_name=_('is started'))
    is_completed = models.BooleanField(default=False, verbose_name=_('is completed'))

    def __str__(self):
        return f"{self.user.get_full_name}-{self.test.title}"
    
    @property
    def get_time_taken(self):
        total_seconds = self.time_taken.total_seconds()
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        return f"{minutes} minut {seconds} sekund"
    
    @property
    def get_total(self):
        total = round(self.score *100 / self.test.number_of_questions, 2)
        return total

class UserAnswer(BaseModel):
    attempt = models.ForeignKey(UserAttempt, related_name="user_answers", on_delete=models.CASCADE, verbose_name=_("attempt"))
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name=_("question"))
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name=_("selected answer"))
    is_correct = models.BooleanField(_("is correct"))

    def __str__(self):
        return f"{self.question.name}-{self.attempt.score}"
    