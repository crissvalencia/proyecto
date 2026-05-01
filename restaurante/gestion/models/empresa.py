from django.db import models


class Empresa(models.Model):

    REGIMEN_CHOICES = [
        ('SIMPLIFICADO',      'Régimen Simplificado'),
        ('COMUN',             'Régimen Común'),
        ('GRAN_CONTRIBUYENTE', 'Gran Contribuyente'),
    ]

    TIPO_IMPUESTO_CHOICES = [
        ('IVA',  'IVA'),
        ('INC',  'INC'),
        ('IBUA', 'IBUA'),
        ('ICL',  'ICL'),
    ]

    razon_social        = models.CharField(max_length=200)
    nombre_comercial    = models.CharField(max_length=200, blank=True)
    nit                 = models.CharField(max_length=20, unique=True)
    direccion           = models.CharField(max_length=300)
    telefono            = models.CharField(max_length=30, blank=True)
    email               = models.EmailField(max_length=100, blank=True)
    logo_url            = models.URLField(max_length=500, blank=True)
    regimen             = models.CharField(max_length=20, choices=REGIMEN_CHOICES)
    tipo_impuesto       = models.CharField(
                            max_length=10,
                            choices=TIPO_IMPUESTO_CHOICES,
                            default='IVA',
                          )
    porcentaje_impuesto = models.DecimalField(
                            max_digits=5,
                            decimal_places=2,
                            default=19.00,
                            help_text='Porcentaje del impuesto. Ejemplo: 19.00 para IVA del 19%',
                          )
    activo              = models.BooleanField(default=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering            = ['razon_social']

    def __str__(self):
        return f"{self.razon_social} — NIT {self.nit}"
