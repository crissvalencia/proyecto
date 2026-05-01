from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        # Depende de la migración anterior que agregó metodo_pago a factura
        ('gestion', '0009_factura_metodo_pago'),
    ]

    operations = [

        # ── 1. Crear tabla gestion_empresa ──────────────────────────────────
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razon_social',        models.CharField(max_length=200)),
                ('nombre_comercial',    models.CharField(blank=True, max_length=200)),
                ('nit',                 models.CharField(max_length=20, unique=True)),
                ('direccion',           models.CharField(max_length=300)),
                ('telefono',            models.CharField(blank=True, max_length=30)),
                ('email',               models.EmailField(blank=True, max_length=100)),
                ('logo_url',            models.URLField(blank=True, max_length=500)),
                ('regimen', models.CharField(
                    choices=[
                        ('SIMPLIFICADO',       'Régimen Simplificado'),
                        ('COMUN',              'Régimen Común'),
                        ('GRAN_CONTRIBUYENTE', 'Gran Contribuyente'),
                    ],
                    max_length=20,
                )),
                ('tipo_impuesto', models.CharField(
                    choices=[
                        ('IVA',  'IVA'),
                        ('INC',  'INC'),
                        ('IBUA', 'IBUA'),
                        ('ICL',  'ICL'),
                    ],
                    default='IVA',
                    max_length=10,
                )),
                ('porcentaje_impuesto', models.DecimalField(
                    decimal_places=2,
                    default=19.0,
                    help_text='Porcentaje del impuesto. Ejemplo: 19.00 para IVA del 19%',
                    max_digits=5,
                )),
                ('activo',     models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name':        'Empresa',
                'verbose_name_plural': 'Empresas',
                'ordering':            ['razon_social'],
            },
        ),

        # ── 2. Crear tabla gestion_sucursal ──────────────────────────────────
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empresa', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='sucursales',
                    to='gestion.empresa',
                )),
                ('nombre',    models.CharField(max_length=150)),
                ('direccion', models.CharField(max_length=300)),
                ('telefono',  models.CharField(blank=True, max_length=30)),
                ('activo',    models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name':        'Sucursal',
                'verbose_name_plural': 'Sucursales',
                'ordering':            ['empresa', 'nombre'],
            },
        ),

        # ── 3. Restricción única: empresa + nombre de sucursal ───────────────
        migrations.AlterUniqueTogether(
            name='sucursal',
            unique_together={('empresa', 'nombre')},
        ),
    ]
