from django.db import migrations, models
import django.db.models.deletion


def asignar_sucursal_a_mesas_huerfanas(apps, schema_editor):
    """
    Antes de aplicar NOT NULL, asegura que toda mesa tenga sucursal.
    Si no existe ninguna sucursal, crea una empresa y sucursal por defecto.
    """
    Mesa = apps.get_model('gestion', 'Mesa')
    Sucursal = apps.get_model('gestion', 'Sucursal')
    Empresa = apps.get_model('gestion', 'Empresa')

    huerfanas = Mesa.objects.filter(sucursal__isnull=True)
    if not huerfanas.exists():
        return  # nada que hacer

    # Obtener o crear una sucursal de respaldo
    sucursal = Sucursal.objects.first()
    if sucursal is None:
        empresa = Empresa.objects.first()
        if empresa is None:
            empresa = Empresa.objects.create(
                razon_social='Restaurante Default',
                nombre_comercial='Restaurante Default',
                nit='0000000000',
                direccion='Dirección por definir',
            )
        sucursal = Sucursal.objects.create(
            empresa=empresa,
            nombre='Sucursal Principal',
            direccion='Dirección por definir',
        )

    huerfanas.update(sucursal=sucursal)


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0025_remove_reserva_uq_reserva_mesa_fecha_hora'),
    ]

    operations = [
        # Paso 1: asignar sucursal a mesas huérfanas
        migrations.RunPython(
            asignar_sucursal_a_mesas_huerfanas,
            reverse_code=migrations.RunPython.noop,
        ),
        # Paso 2: ahora sí, NOT NULL seguro
        migrations.AlterField(
            model_name='mesa',
            name='sucursal',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='mesas',
                to='gestion.sucursal',
            ),
        ),
    ]
