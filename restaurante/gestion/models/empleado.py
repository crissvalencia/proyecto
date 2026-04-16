from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.contrib.auth.models import User


class Empleado(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='empleado')
    PUESTOS = [
        ('mesero', 'Mesero'),
        ('cajero', 'Cajero'),
        ('administrador', 'Administrador'),
    ]
    cedula = models.CharField(
        max_length=20, 
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[1-9]\d*$',
                message='La cédula solo puede contener números y no puede empezar en cero.'
            )
        ]
    )
    nombre = models.CharField(max_length=100)
    puesto = models.CharField(max_length=50, choices=PUESTOS)
    telefono = models.CharField(
        max_length=10, 
        validators=[
            RegexValidator(
                regex=r'^3\d{9}$',
                message='El teléfono debe tener 10 dígitos y empezar por el número 3.'
            )
        ]
    )
    salario = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} (CC: {self.cedula}) - {self.get_puesto_display()}"
