# usuarios/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CustomLoginView, UsuarioCreateView

urlpatterns = [
    path('crear_usuario/', UsuarioCreateView.as_view(), name='crear_usuario'),
]