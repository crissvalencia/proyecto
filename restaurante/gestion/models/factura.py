from django.db import models
from .orden import Orden
from .cliente import Cliente
from .empleado import Empleado


class Factura(models.Model):
    orden = models.OneToOneField(Orden, on_delete=models.CASCADE, related_name='factura')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='facturas')
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='facturas')
    numero_factura = models.CharField(max_length=20, unique=True)
    fecha = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    impuesto = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        ordering = ['-fecha']

    def __str__(self):
        return f"Factura {self.numero_factura}"
