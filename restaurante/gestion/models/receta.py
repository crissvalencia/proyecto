from django.db import models
from django.core.validators import MinValueValidator
from .producto import Producto
from .insumo import Insumo


class Receta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='recetas')
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE, related_name='recetas')
    cantidad_necesaria = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])

    class Meta:
        verbose_name = 'Receta'
        verbose_name_plural = 'Recetas'
        unique_together = ('producto', 'insumo')

    def __str__(self):
        return f"{self.producto.nombre} usa {self.cantidad_necesaria} {self.insumo.unidad_medida} de {self.insumo.nombre}"
