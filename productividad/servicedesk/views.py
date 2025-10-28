# servicedesk/views.py
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse

from .models import Cliente, Categoria, RegistroActividad
from .forms import ClienteForm, CategoriaForm, RegistroActividadForm

# --- CRUD para Clientes ---

class ClienteListView(ListView):
    model = Cliente
    template_name = 'servicedesk/cliente_lista.html'
    context_object_name = 'clientes'

class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'servicedesk/cliente_form.html'
    success_url = reverse_lazy('cliente_lista') # Redirige a la lista tras crear

class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'servicedesk/cliente_form.html'
    success_url = reverse_lazy('cliente_lista') # Redirige a la lista tras editar

class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'servicedesk/cliente_confirm_delete.html'
    success_url = reverse_lazy('cliente_lista')

# --- CRUD para Categorías ---

class CategoriaListView(ListView):
    model = Categoria
    template_name = 'servicedesk/categoria_lista.html'
    context_object_name = 'categorias'

class CategoriaCreateView(CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'servicedesk/categoria_form.html'
    success_url = reverse_lazy('categoria_lista')

class CategoriaUpdateView(UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'servicedesk/categoria_form.html'
    success_url = reverse_lazy('categoria_lista')

class CategoriaDeleteView(DeleteView):
    model = Categoria
    template_name = 'servicedesk/categoria_confirm_delete.html'
    success_url = reverse_lazy('categoria_lista')


# --- VISTA DEL FORMULARIO PRINCIPAL ---

class RegistroActividadCreateView(CreateView):
    model = RegistroActividad
    form_class = RegistroActividadForm
    template_name = 'servicedesk/registro_actividad_form.html'
    success_url = reverse_lazy('registro_crear') # Recarga la misma pág.

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Registrar Actividad'
        return context

# --- VISTA AJAX (LA MAGIA) ---
# Esta vista es llamada por JavaScript, no por un usuario

def cargar_categorias_ajax(request):
    # Obtenemos el ID del cliente del parámetro 'cliente_id' en la URL
    cliente_id = request.GET.get('cliente_id')
    try:
        # Buscamos el cliente
        cliente = Cliente.objects.get(pk=cliente_id)
        # Obtenemos sus categorías permitidas
        categorias = cliente.categorias_permitidas.all()
        # Convertimos las categorías a un formato JSON (lista de diccionarios)
        data = list(categorias.values('id', 'nombre'))
        return JsonResponse(data, safe=False)
    except Cliente.DoesNotExist:
        # Si el cliente no existe (ej. seleccion "---"), devuelve lista vacía
        return JsonResponse([], safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)