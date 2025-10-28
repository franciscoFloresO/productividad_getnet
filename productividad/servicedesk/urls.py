# servicedesk/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # --- URL del Formulario Principal ---
    path('', views.RegistroActividadCreateView.as_view(), name='registro_crear'),

    # --- URL para el AJAX ---
    path('ajax/cargar-categorias/', views.cargar_categorias_ajax, name='cargar_categorias_ajax'),
    
    # --- URLs del CRUD de Clientes ---
    path('clientes/', views.ClienteListView.as_view(), name='cliente_lista'),
    path('clientes/nuevo/', views.ClienteCreateView.as_view(), name='cliente_crear'),
    path('clientes/editar/<int:pk>/', views.ClienteUpdateView.as_view(), name='cliente_editar'),
    path('clientes/borrar/<int:pk>/', views.ClienteDeleteView.as_view(), name='cliente_borrar'),
    
    # --- URLs del CRUD de Categorías ---
    path('categorias/', views.CategoriaListView.as_view(), name='categoria_lista'),
    path('categorias/nueva/', views.CategoriaCreateView.as_view(), name='categoria_crear'),
    path('categorias/editar/<int:pk>/', views.CategoriaUpdateView.as_view(), name='categoria_editar'),
    path('categorias/borrar/<int:pk>/', views.CategoriaDeleteView.as_view(), name='categoria_borrar'),
]