from django.db import models
from django.core.validators import MinValueValidator
from .mesa import Mesa
from .cliente import Cliente
from .empleado import Empleado
from .producto import Producto
from .sucursal import Sucursal          # NUEVO


class Orden(models.Model):

    ESTADOS = [
        ('pendiente',      'Pendiente'),
        ('en_preparacion', 'En Preparación'),
        ('lista',          'Lista'),
        ('pagada',      'Pagada'),
        ('cancelada',      'Cancelada'),
    ]

    # Cada orden pertenece a una sucursal
    sucursal = models.ForeignKey(
        Sucursal,
        on_delete=models.PROTECT,
        related_name='ordenes',
    )
    mesa    = models.ForeignKey(Mesa,     on_delete=models.CASCADE,  related_name='ordenes')
    cliente = models.ForeignKey(Cliente,  on_delete=models.CASCADE,  related_name='ordenes')
    mesero  = models.ForeignKey(Empleado, on_delete=models.CASCADE,  related_name='ordenes')
    estado  = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    total   = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notas   = models.TextField(blank=True)
    fecha               = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Orden'
        verbose_name_plural = 'Ordenes'
        ordering            = ['-fecha']

    def __str__(self):
        return f"Orden #{self.id} — Mesa {self.mesa.numero}"

    def calcular_total(self):
        total = sum(detalle.subtotal for detalle in self.detalles.all())
        self.total = total
        self.save()
        return total


class DetalleOrden(models.Model):

    orden           = models.ForeignKey(Orden,    on_delete=models.CASCADE, related_name='detalles')
    producto        = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='detalles_orden')
    cantidad        = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal        = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name        = 'Detalle de Orden'
        verbose_name_plural = 'Detalles de Orden'

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        self.precio_unitario = self.producto.precio
        self.subtotal        = self.precio_unitario * self.cantidad
        super().save(*args, **kwargs)

        if is_new:
            for receta in self.producto.recetas.all():
                insumo = receta.insumo
                cantidad_a_descontar = receta.cantidad_necesaria * self.cantidad
                if insumo.cantidad < cantidad_a_descontar:
                    raise ValueError(
                        f"Stock insuficiente para '{insumo.nombre}': "
                        f"disponible {insumo.cantidad}, requerido {cantidad_a_descontar}."
                    )
                insumo.cantidad -= cantidad_a_descontar
                insumo.save()

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre}"
