from django.db import models
from django.core.validators import MinValueValidator

class Insumo(models.Model):
    nombre = models.CharField(max_length=100)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    unidad_medida = models.CharField(max_length=20, default='Unidades')
    stock_minimo = models.DecimalField(max_digits=10, decimal_places=2, default=5, validators=[MinValueValidator(0)])
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Insumo'
        verbose_name_plural = 'Insumos'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} - Stock: {self.cantidad} {self.unidad_medida}"
