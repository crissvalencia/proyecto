from django.db import models
from .cliente import Cliente
from .mesa import Mesa


class Reserva(models.Model):
    ESTADOS = [
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('pendiente', 'Pendiente'),
    ]
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='reservas')
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE, related_name='reservas')
    fecha = models.DateField()
    hora = models.TimeField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    duracion = models.PositiveIntegerField(default=2, verbose_name="Duración (horas)")
    num_personas = models.PositiveIntegerField(default=1)
    notas = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['-fecha', '-hora']

    def __str__(self):
        return f"Reserva {self.id} - {self.cliente.nombre} - Mesa {self.mesa.numero}"
