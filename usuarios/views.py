from django.http import JsonResponse
import json
import random
import re

from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Session, Question
from .serializers import SessionSerializer


# Create your views here.
@csrf_exempt
def register_view(request):
    """
    Vista para el registro de usuarios.
    Permite registrar un nuevo usuario en el sistema y crea una sesión asociada a ese usuario.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data["username"]
            email = data["email"]
            password = data["password"]
            confirmation = data["confirmation"]
        except KeyError:
            return JsonResponse({"message": "Invalid JSON data."})

        if not username:
            return JsonResponse({"message": "Nombre de usuario es requerido"})
        if not email:
            return JsonResponse({"message": "Correo electróncio es requerido"})
        if not re.match(r'^[a-zA-Z\w\.-]+@[\w\.-]+\.\w+$', email):
            return JsonResponse({"message": "Correo electrónico inválido"})
        if User.objects.filter(email=email).exists():
            return JsonResponse({"message": "El correo electrónico ya está vinculado"})
        if password != confirmation:
            return JsonResponse({"message": "Contraseñas no coinciden"})

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            session = Session.objects.create(user=user)
            preguntas_disponibles = Question.objects.all()
            cantidad_preguntas = preguntas_disponibles.count()
            if cantidad_preguntas >= 5:
                preguntas_seleccionadas = random.sample(list(preguntas_disponibles), 5)
            else:
                preguntas_seleccionadas = preguntas_disponibles
            session.questions.set(preguntas_seleccionadas)
            session.save()
            session = SessionSerializer(instance=session)
        except IntegrityError:
            return JsonResponse({"message": "Username already taken."})

        login(request, user)
        return JsonResponse(
            {"message": "Registration successful.", "id": user.id, "username": user.username, "session": session.data})
    else:
        return JsonResponse({"message": "Only POST request are allowed"}, status=405)


@csrf_exempt
def login_view(request):
    """
    Vista para iniciar sesión.
    Permite que un usuario inicie sesión en el sistema y actualiza la sesión asociada a ese usuario si es necesario.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data["email"]
            password = data["password"]
        except KeyError:
            return JsonResponse({"message": "Invalid JSON data."})
        User = get_user_model()
        user = User.objects.filter(email=email).first()
        if user is not None and user.check_password(password):
            login(request, user)
            session, _ = Session.objects.get_or_create(user=user)
            if(len(SessionSerializer(instance=session).data["questions"])):
                preguntas_disponibles = Question.objects.all()
                cantidad_preguntas = preguntas_disponibles.count()
                if cantidad_preguntas >= 5:
                    preguntas_seleccionadas = random.sample(list(preguntas_disponibles), 5)
                else:
                    preguntas_seleccionadas = preguntas_disponibles

                session.questions.set(preguntas_seleccionadas)
                session.save()

            if session.Evaluacion == 5:
                preguntas_disponibles = Question.objects.all()
                cantidad_preguntas = preguntas_disponibles.count()
                if cantidad_preguntas >= 5:
                    preguntas_seleccionadas = random.sample(list(preguntas_disponibles), 5)
                else:
                    preguntas_seleccionadas = preguntas_disponibles

                session.questions.set(preguntas_seleccionadas)
                session.Evaluacion = 0
                session.save()
            session = SessionSerializer(instance=session)
            return JsonResponse(
                {"message": "Login successful", "id": user.id, "username": user.username, "session": session.data})
        else:
            return JsonResponse({"message": "Invalid email and/or password."})

    else:
        return JsonResponse({"message": "Only POST requests are allowed"}, status=405)


@csrf_exempt
def get_users_view(request):
    """
    Vista para obtener la lista de usuarios.
    Devuelve una lista con todos los usuarios registrados en el sistema.
    """
    users = User.objects.all().values()
    return JsonResponse(list(users), safe=False)


@csrf_exempt
def update_session(request):
    """
    Vista para actualizar una sesión.
    Permite actualizar los datos de una sesión en el sistema.
    """
    if request.method == "PUT":
        data = json.loads(request.body)
        answers = data["answers"]
        session = Session.objects.get(pk=data["id"])
        session.lastPage = data["lastPage"]
        session.Landing = data["Landing"]
        session.Destacado = data["Destacado"]
        session.Arquitectura = data["Arquitectura"]
        session.Museo = data["Museo"]
        session.Gastronomía = data["Gastronomía"]
        session.Evaluacion = data["Evaluacion"]
        session.answer1 = answers["answer1"]
        session.answer2 = answers["answer2"]
        session.answer3 = answers["answer3"]
        session.answer4 = answers["answer4"]
        session.answer5 = answers["answer5"]
        if session.Evaluacion == 5:
            preguntas_disponibles = Question.objects.all()
            cantidad_preguntas = preguntas_disponibles.count()
            if cantidad_preguntas >= 5:
                preguntas_seleccionadas = random.sample(list(preguntas_disponibles), 5)
            else:
                preguntas_seleccionadas = preguntas_disponibles

            session.questions.set(preguntas_seleccionadas)
            session.Evaluacion = 0
        session.save()
        return JsonResponse({"message": "Session updated successfully.", "session": SessionSerializer(instance=session).data}, status=200)
    else:
        return JsonResponse({"message": "Only PUT requests are allowed."}, status=405)

@csrf_exempt
def conect_view(request):
    """
    Vista para verificar la conexión con el servidor.
    Devuelve un mensaje de éxito para confirmar que el servidor está funcionando correctamente.
    """
    if request.method == "GET":
        return JsonResponse(
            {"message": "Server started successfully."},
            status=200)