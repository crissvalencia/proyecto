from django.db import models
from django.core.exceptions import ValidationError
import datetime
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

    def clean(self):
        """Valida solapamiento de horarios a nivel de modelo (protege toda inserción a la BD)."""
        if not self.mesa or not self.fecha or not self.hora or not self.duracion:
            return

        if self.estado not in ['confirmada', 'pendiente']:
            return

        nueva_inicio = datetime.datetime.combine(self.fecha, self.hora)
        nueva_fin = nueva_inicio + datetime.timedelta(hours=self.duracion)

        reservas_dia = Reserva.objects.filter(
            mesa=self.mesa,
            fecha=self.fecha,
            estado__in=['confirmada', 'pendiente']
        )
        if self.pk:
            reservas_dia = reservas_dia.exclude(pk=self.pk)

        for r in reservas_dia:
            r_inicio = datetime.datetime.combine(r.fecha, r.hora)
            r_fin = r_inicio + datetime.timedelta(hours=r.duracion)
            if r_inicio < nueva_fin and r_fin > nueva_inicio:
                raise ValidationError(
                    f"Conflicto de horario: La mesa {self.mesa.numero} ya tiene una "
                    f"reserva de {r.hora.strftime('%I:%M %p')} a {r_fin.strftime('%I:%M %p')} "
                    f"en esa fecha."
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
