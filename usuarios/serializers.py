from rest_framework import serializers
from .models import Question, Session


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ("id", "utterance", "answer", "opt1", "opt2", "opt3", "opt4", "feedback")


class SessionSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    class Meta:
        model = Session
        fields = ("id", "user", "lastPage", "Landing", "Destacado", "Arquitectura", "Museo", "Gastronomía", "Evaluacion", "questions")

