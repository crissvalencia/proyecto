
import os
import django
import sys

# Add project root to path
sys.path.append('c:/Users/Usuario/.gemini/antigravity/scratch/restaurante')

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurante.settings')
django.setup()

from gestion.models import Empleado

def verify_employee():
    print("Checking existing employees...")
    initial_count = Empleado.objects.count()
    print(f"Initial count: {initial_count}")

    print("Creating test employee...")
    nuevo = Empleado(
        nombre='Test Employee',
        puesto='mesero',
        telefono='1234567890',
        salario=1500.00,
        activo=True
    )
    nuevo.save()
    print(f"Created employee with ID: {nuevo.id}")

    print("Verifying in database...")
    empleados = Empleado.objects.all()
    print(f"Current count: {empleados.count()}")
    
    found = False
    for emp in empleados:
        print(f"- {emp.nombre} ({emp.puesto})")
        if emp.id == nuevo.id and emp.nombre == 'Test Employee':
            found = True
            
    if found:
        print("\nSUCCESS: New employee found in database.")
    else:
        print("\nFAILURE: New employee NOT found.")

if __name__ == '__main__':
    verify_employee()
