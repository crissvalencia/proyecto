from django.shortcuts import render
from gestion.models import Empleado, Producto, Orden, Reserva, Cliente, Mesa, Insumo
from django.utils import timezone
from django.db.models import F


def dashboard(request):
    context = {
        'total_empleados': Empleado.objects.filter(activo=True).count(),
        'total_productos': Producto.objects.count(),
        'total_ordenes': Orden.objects.exclude(estado='cancelada').count(),
        'total_reservas': Reserva.objects.filter(estado='confirmada').count(),
        'total_clientes': Cliente.objects.count(),
        'total_mesas': Mesa.objects.count(),
        'ordenes_recientes': Orden.objects.order_by('-fecha')[:5],
        'reservas_hoy': Reserva.objects.filter(fecha=timezone.now().date()),
        'insumos_bajo_stock': Insumo.objects.filter(cantidad__lte=F('stock_minimo')),
    }
    return render(request, 'gestion/dashboard.html', context)
