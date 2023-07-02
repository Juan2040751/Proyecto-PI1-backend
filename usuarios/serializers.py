from rest_framework import serializers
from .models import Question, Session


class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Question.
    Transforma la información de la base de datos en un formato adecuado para enviar a la interfaz.
    """
    options = serializers.SerializerMethodField()
    class Meta:
        model = Question
        fields = ("id", "utterance", "answer", "options", "feedback")
    def get_options(self, obj):
        """
        Método para obtener las opciones de respuesta de una pregunta.
        """
        return {"opt1": obj.opt1,"opt2": obj.opt2, "opt3": obj.opt3, "opt4": obj.opt4}
class SessionSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Session.
    Transforma la información de la base de datos en un formato adecuado para enviar a la interfaz.
    """
    questions = QuestionSerializer(many=True, read_only=True)
    answers = serializers.SerializerMethodField()
    class Meta:
        model = Session
        fields = ("id", "user", "lastPage", "Landing", "Destacado", "Arquitectura", "Museo", "Gastronomía", "Evaluacion", "questions", "answers")
    def get_answers(self, obj):
        """
        Método para obtener las respuestas del usuario para las preguntas de una sesión.
        """
        return {"answer1": obj.answer1,"answer2": obj.answer2, "answer3": obj.answer3, "answer4": obj.answer4,"answer5": obj.answer5}
