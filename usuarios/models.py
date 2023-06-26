from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    utterance = models.CharField(max_length=5000)
    answerChoice = [("opt1", "opt1"), ("opt2", "opt2"), ("opt3", "opt3"), ("opt4", "opt4")]
    answer = models.CharField(choices=answerChoice, max_length=4)
    opt1 = models.CharField(max_length=2000)
    opt2 = models.CharField(max_length=2000)
    opt3 = models.CharField(max_length=2000)
    opt4 = models.CharField(max_length=2000)
    feedback = models.CharField(max_length=5000)

class Session(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    lastPageChoices = [("Landing", "Landing"), ("Destacado", "Destacado"), ("Arquitectura", "Arquitectura"),
                       ("Museo", "Museo"), ("Gastronomía", "Gastronomía"), ("Evaluacion", "Evaluacion")]
    lastPage = models.CharField(choices=lastPageChoices, default="Landing", max_length=16)
    lastCardChoices = [(-1, -1), (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    questions = models.ManyToManyField(Question, related_name="questions")
    Landing = models.IntegerField(choices=lastCardChoices, default=-1)
    Destacado = models.IntegerField(choices=lastCardChoices, default=0)
    Arquitectura = models.IntegerField(choices=lastCardChoices, default=0)
    Museo = models.IntegerField(choices=lastCardChoices, default=0)
    Gastronomía = models.IntegerField(choices=lastCardChoices, default=0)
    Evaluacion = models.IntegerField(choices=lastCardChoices, default=0)

# Create your models here.
