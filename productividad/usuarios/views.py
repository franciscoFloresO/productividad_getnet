# usuarios/views.py
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import CustomUserCreationForm
from django.contrib.auth import views as auth_views

# Usamos Vistas Basadas en Clases (CBV)
# LoginRequiredMixin: Asegura que el usuario haya iniciado sesión.
# PermissionRequiredMixin: Asegura que el usuario tenga el permiso.

class UsuarioCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'usuarios/crear_usuario_form.html'
    success_url = reverse_lazy('cliente_lista') # O a donde quieras ir
    
    # --- ¡ESTA ES LA PROTECCIÓN! ---
    permission_required = 'auth.add_user'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Crear Nuevo Usuario'
        return context
    

class CustomLoginView(auth_views.LoginView):
    template_name = 'usuarios/login.html'
    redirect_authenticated_user = True