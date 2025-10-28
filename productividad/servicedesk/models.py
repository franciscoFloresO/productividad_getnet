# servicedesk/models.py
from django.db import models

class Categoria(models.Model):
    # Catálogo de TODAS las categorías posibles que existen
    nombre = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    # Catálogo de Clientes
    nombre = models.CharField(max_length=100, unique=True)

    categorias_permitidas = models.ManyToManyField(
        Categoria,
        verbose_name="Categorías Permitidas",
        # 'blank=True' permite que un cliente se cree sin categorías
        blank=True, 
        related_name="clientes"
    )

    def __str__(self):
        return self.nombre

class RegistroActividad(models.Model):
    # Este es el modelo de TU FORMULARIO (el "log" del evento)
    
    class Origen(models.TextChoices):
        EMAIL = 'email', 'Email'
        TELEFONO = 'telefono', 'Teléfono'
        OTROS = 'otros', 'Otros'

    # Un registro pertenece a UN solo cliente
    cliente = models.ForeignKey(
        Cliente, 
        on_delete=models.CASCADE, 
        verbose_name="Cliente"
    )
    
    # Un registro usa UNA sola categoría
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.CASCADE, 
        verbose_name="Categoría"
    )
    
    # Los otros campos del formulario
    origen_contacto = models.CharField(
        max_length=10,
        choices=Origen.choices,
        default=Origen.EMAIL,
        verbose_name="Origen del contacto"
    )
    
    comentarios = models.TextField(blank=True, null=True, verbose_name="Comentarios")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Registro de Actividad"
        verbose_name_plural = "Registros de Actividad"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Registro de {self.cliente.nombre} - {self.categoria.nombre}"