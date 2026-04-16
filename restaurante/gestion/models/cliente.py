from django.db import models
from django.core.validators import RegexValidator


class Cliente(models.Model):
    cedula = models.CharField(
        max_length=20, 
        unique=True, 
        default="0",
        validators=[
            RegexValidator(
                regex=r'^[1-9]\d*$',
                message='La cédula solo puede contener números y no puede empezar en cero.'
            )
        ]
    )
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(
        max_length=10, 
        validators=[
            RegexValidator(
                regex=r'^3\d{9}$',
                message='El teléfono debe tener 10 dígitos y empezar por el número 3.'
            )
        ]
    )
    email = models.EmailField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} (CC: {self.cedula})"
