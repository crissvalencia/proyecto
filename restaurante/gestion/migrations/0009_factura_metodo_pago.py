from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        # Ajusta este número al nombre de la última migración existente en tu proyecto.
        # Actualmente la última es 0008_alter_empleado_puesto
        ('gestion', '0008_alter_empleado_puesto'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='metodo_pago',
            field=models.CharField(
                choices=[
                    ('efectivo',      'Efectivo'),
                    ('tarjeta',       'Tarjeta'),
                    ('transferencia', 'Transferencia'),
                ],
                default='efectivo',
                max_length=20,
                verbose_name='Método de pago',
            ),
        ),
    ]
