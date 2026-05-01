from django.db import models
from django.core.validators import RegexValidator


class Cliente(models.Model):

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

    nombre = models.CharField(max_length=100)

    telefono = models.CharField(
        max_length=10,
        blank=False,
        validators=[
            RegexValidator(
                regex=r'^3\d{9}$',
                message='El teléfono debe tener 10 dígitos y empezar por el número 3.'
            )
        ]
    )

    email = models.EmailField(max_length=255, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_documento_display()}: {self.numero_documento})"
