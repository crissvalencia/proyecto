from django.db import models
from .empresa import Empresa


class Sucursal(models.Model):

    empresa    = models.ForeignKey(
                   Empresa,
                   on_delete=models.CASCADE,
                   related_name='sucursales',
                 )
    nombre     = models.CharField(max_length=150)
    direccion  = models.CharField(max_length=300)
    telefono   = models.CharField(max_length=30, blank=True)
    activo     = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Sucursal'
        verbose_name_plural = 'Sucursales'
        ordering            = ['empresa', 'nombre']
        # Una empresa no puede tener dos sucursales con el mismo nombre
        unique_together     = [('empresa', 'nombre')]

    def __str__(self):
        return f"{self.empresa.nombre_comercial or self.empresa.razon_social} — {self.nombre}"
