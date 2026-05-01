from django.db import models
from .sucursal import Sucursal


class Mesa(models.Model):
    sucursal   = models.ForeignKey(
        Sucursal,
        on_delete=models.CASCADE,
        related_name='mesas',
    )
    numero     = models.PositiveIntegerField()
    capacidad  = models.PositiveIntegerField(default=4)
    disponible = models.BooleanField(default=True)

    class Meta:
        verbose_name        = 'Mesa'
        verbose_name_plural = 'Mesas'
        ordering            = ['sucursal', 'numero']
        unique_together     = [('sucursal', 'numero')]  # ← reemplaza el unique=True global

    def __str__(self):
        return f"Mesa {self.numero} (Cap. {self.capacidad})"

    @property
    def has_reservation_today(self):
        # Si mesa_list hizo prefetch con to_attr='_reservas_hoy', usamos ese
        # cache (0 queries extra). Si se llama desde otro contexto, hacemos
        # el query normal. Incluye 'pendiente' consistente con Reserva.clean().
        if hasattr(self, '_reservas_hoy'):
            return len(self._reservas_hoy) > 0
        from django.utils import timezone
        today = timezone.localdate()
        return self.reservas.filter(
            fecha=today, estado__in=['confirmada', 'pendiente']
        ).exists()
