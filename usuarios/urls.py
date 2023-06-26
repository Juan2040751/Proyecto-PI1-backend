from django.urls import path
from . import views

urlpatterns = [
    path("registro", views.register_view, name="registro"),
    path("sesion", views.update_session, name="sesion"),
    path("login", views.login_view, name="login"),
    path("getUsuarios", views.get_users_view, name="getUsuarios"),
]