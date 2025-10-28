# usuarios/forms.py
from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    # Añadimos un campo extra para seleccionar el grupo
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        label="Grupo"
    )

    class Meta(UserCreationForm.Meta):
        model = User
        # Definimos los campos que queremos en el formulario
        fields = ('username', 'first_name', 'last_name', 'email')

    def save(self, commit=True):
        # Guardamos el usuario (esto hashea la contraseña, etc.)
        user = super().save(commit=False)
        
        # Guardamos los campos extra
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        
        if commit:
            user.save()
            # Añadimos el usuario al grupo seleccionado
            grupo_seleccionado = self.cleaned_data["grupo"]
            user.groups.add(grupo_seleccionado)
            
        return user