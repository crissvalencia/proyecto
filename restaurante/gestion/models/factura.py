from django.db import models
from .orden import Orden
from .cliente import Cliente
from .empleado import Empleado
from .sucursal import Sucursal          # NUEVO


class Factura(models.Model):

    METODOS_PAGO = [
        ('efectivo',      'Efectivo'),
        ('tarjeta',       'Tarjeta'),
        ('transferencia', 'Transferencia'),
    ]

    orden    = models.OneToOneField(Orden,    on_delete=models.CASCADE, related_name='factura')
    cliente  = models.ForeignKey(Cliente,     on_delete=models.CASCADE, related_name='facturas')
    empleado = models.ForeignKey(Empleado,    on_delete=models.CASCADE, related_name='facturas')

    # Sucursal que emite la factura
    # — desde aquí se sube a empresa para obtener NIT y razón social
    sucursal = models.ForeignKey(
        Sucursal,
        on_delete=models.PROTECT,
        related_name='facturas',
    )

    numero_factura      = models.CharField(max_length=20, unique=True)
    fecha               = models.DateTimeField(auto_now_add=True)
    subtotal            = models.DecimalField(max_digits=12, decimal_places=2)
    impuesto            = models.DecimalField(max_digits=12, decimal_places=2)
    total               = models.DecimalField(max_digits=12, decimal_places=2)
    metodo_pago         = models.CharField(
                            max_length=20,
                            choices=METODOS_PAGO,
                            default='efectivo',
                          )

    monto_recibido       = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    vuelto               = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    numero_aprobacion    = models.CharField(max_length=50, null=True, blank=True)
    numero_transferencia = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name        = 'Factura'
        verbose_name_plural = 'Facturas'
        ordering            = ['-fecha']

    def __str__(self):
        return f"Factura {self.numero_factura}"
