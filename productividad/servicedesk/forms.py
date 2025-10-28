# servicedesk/forms.py
from django import forms
from .models import RegistroActividad, Cliente, Categoria

# --- 1. Formulario para el CRUD de Clientes ---
# Este formulario manejará el ManyToManyField como checkboxes

class ClienteForm(forms.ModelForm):
    
    # Sobrescribimos el campo para usar un widget de checkboxes
    categorias_permitidas = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,  # Permite crear un cliente sin categorías
        label="Categorías Permitidas"
    )

    class Meta:
        model = Cliente
        fields = ['nombre', 'categorias_permitidas']
        labels = {
            'nombre': 'Nombre del Cliente',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }


# --- 2. Formulario para el CRUD de Categorías ---
# Este es un formulario muy simple

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        labels = {
            'nombre': 'Nombre de la Categoría',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }


# --- 3. Formulario Principal de Registro de Actividad ---
# Este es el formulario de tu imagen. Es el más complejo.

class RegistroActividadForm(forms.ModelForm):
    class Meta:
        model = RegistroActividad
        fields = ['cliente', 'categoria', 'origen_contacto', 'comentarios']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'origen_contacto': forms.Select(attrs={'class': 'form-control'}),
            'comentarios': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        """
        Esto es clave para tu lógica de "selects dependientes".
        """
        super().__init__(*args, **kwargs)

        # 1. Hacemos que el queryset de 'categoria' esté vacío por defecto.
        self.fields['categoria'].queryset = Categoria.objects.none()

        # 2. Comprobamos si el formulario ya tiene un 'cliente' seleccionado
        #    (ya sea porque se está editando o porque se envió por POST)

        if 'cliente' in self.data:
            # Caso 1: El formulario se está enviando (POST)
            try:
                cliente_id = int(self.data.get('cliente'))
                # Filtramos el queryset de categorías
                cliente = Cliente.objects.get(pk=cliente_id)
                self.fields['categoria'].queryset = cliente.categorias_permitidas.all()
            except (ValueError, TypeError, Cliente.DoesNotExist):
                pass # El cliente no es válido, queryset sigue vacío
        
        elif self.instance.pk and self.instance.cliente:
            # Caso 2: El formulario se está editando (UpdateView)
            # Filtramos por las categorías del cliente que ya está guardado
            self.fields['categoria'].queryset = self.instance.cliente.categorias_permitidas.all()