import os
import django

def crear_rol_mesero():
    print("Configurando entorno Django...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurante.settings')
    django.setup()

    from django.contrib.auth.models import Group, Permission

    # Definimos los permisos exactos que hablamos
    permisos_codenames = [
        'add_orden',
        'change_orden',
        'view_orden',
        'view_mesa',
        'view_producto'
    ]

    print("Buscando o creando el grupo 'Meseros'...")
    # Creamos o conseguimos el grupo "Meseros"
    grupo_meseros, created = Group.objects.get_or_create(name='Meseros')

    print("Buscando los permisos...")
    # Buscamos los permisos en la app 'gestion'
    permisos = Permission.objects.filter(
        content_type__app_label='gestion',
        codename__in=permisos_codenames
    )

    if not permisos.exists():
        print("ERROR: No se encontraron los permisos. ¿Has ejecutado las migraciones (makemigrations/migrate)?")
        return

    # Añadimos los permisos al grupo
    grupo_meseros.permissions.set(permisos)
    grupo_meseros.save()

    if created:
        print(f"¡ÉXITO! Grupo 'Meseros' creado con {permisos.count()} permisos:")
    else:
        print(f"¡ÉXITO! Grupo 'Meseros' actualizado con {permisos.count()} permisos:")
    
    for p in permisos:
        print(f" - {p.name} ({p.codename})")

if __name__ == '__main__':
    crear_rol_mesero()
