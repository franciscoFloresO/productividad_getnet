# servicedesk/admin.py
from django.contrib import admin
from .models import Cliente, Categoria, RegistroActividad

# --- Opción 1: Editar categorías desde el Cliente (La que ya tenías) ---

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    
    # Esto SÍ está correcto y usa el widget de filtro horizontal
    filter_horizontal = ['categorias_permitidas']

# --- Opción 2: Editar clientes desde la Categoría (La forma correcta) ---

# 1. Definimos el "Inline". 
# Le decimos a Django que use la tabla intermedia automática
# que se creó para el ManyToManyField.
class ClienteInline(admin.TabularInline):
    model = Cliente.categorias_permitidas.through # <-- Esta es la clave
    verbose_name = "Cliente asociado"
    verbose_name_plural = "Clientes asociados"
    extra = 1 # Muestra 1 campo vacío para agregar uno nuevo

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    
    # 2. Quitamos la línea que daba error:
    # filter_horizontal = ['clientes'] # <-- ESTA LÍNEA SE BORRA
    
    # 3. Agregamos el Inline que definimos arriba
    inlines = [ClienteInline]

# --- Registro del modelo de formulario (sigue igual) ---
admin.site.register(RegistroActividad)