from django.db import models


class Mesa(models.Model):
    numero = models.PositiveIntegerField(unique=True)
    capacidad = models.PositiveIntegerField(default=4)
    disponible = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Mesa'
        verbose_name_plural = 'Mesas'
        ordering = ['numero']

    def __str__(self):
        return f"Mesa {self.numero} (Cap. {self.capacidad})"

    @property
    def has_reservation_today(self):
        from .reserva import Reserva
        from django.utils import timezone
        today = timezone.localdate()
        return self.reservas.filter(fecha=today, estado__in=['confirmada']).exists()
