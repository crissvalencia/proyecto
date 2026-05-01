from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0017_alter_cliente_cedula_alter_empleado_cedula'),
    ]

    operations = [
        migrations.AddField(
            model_name='empleado',
            name='tipo_documento',
            field=models.CharField(
                max_length=5,
                choices=[
                    ('CC',  'Cédula de Ciudadanía'),
                    ('PPT', 'Permiso de Protección Temporal'),
                    ('PEP', 'Permiso Especial de Permanencia'),
                    ('CE',  'Cédula de Extranjería'),
                    ('PA',  'Pasaporte'),
                ],
                default='CC',
                verbose_name='Tipo de documento',
            ),
        ),
        migrations.AddField(
            model_name='empleado',
            name='numero_documento',
            field=models.CharField(
                max_length=20,
                unique=False,
                default='',
                verbose_name='Número de documento',
            ),
            preserve_default=False,
        ),
        migrations.RunSQL(
            sql="UPDATE gestion_empleado SET numero_documento = cedula;",
            reverse_sql="UPDATE gestion_empleado SET cedula = numero_documento;",
        ),
        migrations.AlterField(
            model_name='empleado',
            name='numero_documento',
            field=models.CharField(
                max_length=20,
                unique=True,
                verbose_name='Número de documento',
            ),
        ),
        migrations.RemoveField(
            model_name='empleado',
            name='cedula',
        ),
    ]
