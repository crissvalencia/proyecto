from django.db import models
from django.core.validators import MinValueValidator
from .categoria import Categoria

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='productos'
    )
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"