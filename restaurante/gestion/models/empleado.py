from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.contrib.auth.models import User
from .sucursal import Sucursal

class Empleado(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='empleado')
    PUESTOS = [
        ('mesero', 'Mesero'),
        ('cajero', 'Cajero'),
        ('administrador', 'Administrador'),
    ]
    
    # NUEVO: sucursal donde trabaja el empleado
    sucursal = models.ForeignKey(
        'Sucursal',
        on_delete=models.SET_NULL,
        related_name='empleados',
        null=True,
        blank=True,
        verbose_name='Sucursal',
    )

    TIPO_DOCUMENTO_CHOICES = [
        ('CC',  'Cédula de Ciudadanía'),
        ('PPT', 'Permiso de Protección Temporal'),
        ('PEP', 'Permiso Especial de Permanencia'),
        ('CE',  'Cédula de Extranjería'),
        ('PA',  'Pasaporte'),
    ]

    tipo_documento = models.CharField(
        max_length=5,
        choices=TIPO_DOCUMENTO_CHOICES,
        default='CC',
        verbose_name='Tipo de documento',
    )

    numero_documento = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Número de documento',
    )
    nombre = models.CharField(max_length=100, verbose_name='Nombres')
    apellido = models.CharField(max_length=100, verbose_name='Apellidos')
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
        return f"{self.nombre} {self.apellido} ({self.get_tipo_documento_display()}: {self.numero_documento}) - {self.get_puesto_display()}"
