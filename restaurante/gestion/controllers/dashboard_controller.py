from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from gestion.models import Empleado, Producto, Orden, Reserva, Cliente, Mesa, Insumo, Factura
from django.utils import timezone
from django.db.models import F, Sum


@login_required(login_url='/login/')
def dashboard(request):
    hoy = timezone.now().date()

    # ── RF0010: 4 métricas requeridas ────────────────────────────────────────
    ordenes_activas = Orden.objects.filter(
        estado__in=['pendiente', 'en_preparacion', 'lista']
    ).count()

    mesas_ocupadas = Mesa.objects.filter(disponible=False).count()

    ventas_hoy = Factura.objects.filter(
        fecha__date=hoy
    ).aggregate(total=Sum('total'))['total'] or 0

    productos_mas_vendidos = (
        Producto.objects
        .filter(detalles_orden__orden__fecha__date=hoy)
        .annotate(total_vendido=Sum('detalles_orden__cantidad'))
        .order_by('-total_vendido')[:5]
    )
    # ─────────────────────────────────────────────────────────────────────────

    context = {
        # Conteos generales de la vista
        'total_empleados':    Empleado.objects.filter(activo=True).count(),
        'total_productos':    Producto.objects.count(),
        'total_reservas':     Reserva.objects.filter(estado='confirmada').count(),
        'total_clientes':     Cliente.objects.count(),
        'total_mesas':        Mesa.objects.count(),
        'ordenes_recientes':  Orden.objects.order_by('-fecha')[:5],
        'reservas_hoy':       Reserva.objects.filter(fecha=hoy),
        'insumos_bajo_stock': Insumo.objects.filter(cantidad__lte=F('stock_minimo')),

        # RF0010
        'ordenes_activas':        ordenes_activas,
        'mesas_ocupadas':         mesas_ocupadas,
        'ventas_hoy':             ventas_hoy,
        'productos_mas_vendidos': productos_mas_vendidos,
    }
    return render(request, 'gestion/dashboard.html', context)
