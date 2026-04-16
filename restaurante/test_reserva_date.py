import os
import django
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurante.settings')
django.setup()

from gestion.helpers.forms import ReservaForm
from gestion.models import Cliente, Mesa

try:
    cliente = Cliente.objects.first()
    mesa = Mesa.objects.first()

    if not cliente or not mesa:
        print("No cliente or mesa found in DB. Test might behave unexpectedly if fields are strictly required.")

    # Test past date
    past_date = datetime.date.today() - datetime.timedelta(days=1)
    
    data_past = {
        'cliente': cliente.id if cliente else 1,
        'mesa': mesa.id if mesa else 1,
        'fecha': past_date.strftime('%Y-%m-%d'),
        'hora': '12:00',
        'duracion': 2,
        'estado': 'pendiente',
        'num_personas': 2,
        'notas': 'Test past',
    }
    
    form_past = ReservaForm(data=data_past)
    print("Testing past date:", past_date)
    print("form_past.is_valid():", form_past.is_valid())
    if form_past.errors:
        print("Errors for past date:", form_past.errors)

    # Test today
    today_date = datetime.date.today()
    data_today = data_past.copy()
    data_today['fecha'] = today_date.strftime('%Y-%m-%d')
    
    form_today = ReservaForm(data=data_today)
    print("\nTesting today:", today_date)
    print("form_today.is_valid():", form_today.is_valid())
    if form_today.errors:
        print("Errors for today:", form_today.errors)

except Exception as e:
    print(f"Error checking forms: {e}")
