from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0010_empresa_sucursal'),
    ]

    operations = [

        # ── Paso 1: sucursal_id en gestion_orden ────────────────────────────
        migrations.AddField(
            model_name='orden',
            name='sucursal',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='ordenes',
                to='gestion.sucursal',
                verbose_name='Sucursal',
            ),
        ),

        # ── Paso 2: sucursal_id en gestion_factura ──────────────────────────
        migrations.AddField(
            model_name='factura',
            name='sucursal',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='facturas',
                to='gestion.sucursal',
                verbose_name='Sucursal',
            ),
        ),
    ]
