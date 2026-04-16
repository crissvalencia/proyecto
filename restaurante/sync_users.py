import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurante.settings')
django.setup()

from gestion.models import Empleado
from django.contrib.auth.models import User

for emp in Empleado.objects.all():
    if not emp.usuario:
        # Usernames must be unique, so if someone deleted an employee and recreating, handle it
        user, created = User.objects.get_or_create(username=emp.cedula)
        if created:
            user.set_password(emp.cedula)
            user.save()
        emp.usuario = user
        emp.save()
        print(f"Usuario '{emp.cedula}' creado/asociado para {emp.nombre} - Rol: {emp.puesto}")

# Also create an explicit admin if none exists
if not Empleado.objects.filter(puesto='administrador').exists():
    admin_user, created = User.objects.get_or_create(username='admin')
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
    admin_emp = Empleado.objects.create(
        cedula='9999999999',
        nombre='Administrador General',
        puesto='administrador',
        telefono='3000000000',
        salario=1000,
        usuario=admin_user
    )
    print("Se creó el usuario 'admin' con clave 'admin123' y rol administrador para pruebas.")

print("Sincronización completa.")
