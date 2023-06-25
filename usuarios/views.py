from django.shortcuts import render
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import MultiValueDict
from django.contrib.auth.models import User
from .models import Session, Question
from .serializers import SessionSerializer
import random
from django.db.models import Count
import json
import re

# Create your views here.
@csrf_exempt
def register_view(request):
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
        return JsonResponse({"message": "Registration successful.", "id": user.id, "username": user.username, "session": session.data})
    else:
        return JsonResponse({"message": "Only POST request are allowed"}, status=405)
    

@csrf_exempt
def login_view(request):
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
            return JsonResponse({"message": "Login successful", "id": user.id, "username": user.username, "session": session.data})
        else:
            return JsonResponse({"message": "Invalid email and/or password."})

    else:
        return JsonResponse({"message": "Only POST requests are allowed"}, status=405)


@csrf_exempt
def get_users_view(request):
    users = User.objects.all().values()
    return JsonResponse(list(users), safe=False)