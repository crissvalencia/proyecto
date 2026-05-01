from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0021_factura_detalle_transaccion_rf005'),
    ]

    operations = [
        # Paso 1: quitar el unique global de numero
        migrations.AlterField(
            model_name='mesa',
            name='numero',
            field=models.PositiveIntegerField(),
        ),
        # Paso 2: agregar la FK a sucursal
        migrations.AddField(
            model_name='mesa',
            name='sucursal',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='mesas',
                to='gestion.sucursal',
            ),
        ),
        # Paso 3: unique_together reemplaza al unique=True
        migrations.AlterUniqueTogether(
            name='mesa',
            unique_together={('sucursal', 'numero')},
        ),
    ]
