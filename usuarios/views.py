from django.shortcuts import render
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import MultiValueDict
from django.contrib.auth.models import User
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
        except IntegrityError:
            return JsonResponse({"message": "Username already taken."})
        
        login(request, user)
        return JsonResponse({"message": "Registration successful.", "id": user.id, "username": user.username})
    else:
        return JsonResponse({"message": "Only POST request are allowed"}, status=405)
    

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data["email"]
            password = data["password"]
            print(email, password)
        except KeyError:
            return JsonResponse({"message": "Invalid JSON data."})

        User = get_user_model()
        user = User.objects.filter(email=email).first()

        if user is not None and user.check_password(password):
            login(request, user)
            return JsonResponse({"message": "Login successful", "id": user.id, "username": user.username})
        else:
            return JsonResponse({"message": "Invalid email and/or password."})

    else:
        return JsonResponse({"message": "Only POST requests are allowed"}, status=405)


@csrf_exempt
def get_users_view(request):
    users = User.objects.all().values()
    return JsonResponse(list(users), safe=False)