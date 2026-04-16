from django.shortcuts import render, get_object_or_404
from gestion.models import Factura


def generar_factura_auto(orden):
    if not orden.cliente or not orden.mesero:
        raise ValueError("No se puede generar la factura: la orden en cuestión no tiene un cliente o mesero asignado.")
        
    subtotal = orden.total
    impuesto = subtotal * 0.19
    total = subtotal + impuesto
    ultimo = Factura.objects.order_by('-id').first()
    numero = f"FAC-{(ultimo.id + 1 if ultimo else 1):06d}"
    Factura.objects.create(
        orden=orden, cliente=orden.cliente, empleado=orden.mesero,
        numero_factura=numero, subtotal=subtotal, impuesto=impuesto, total=total,
    )


def factura_list(request):
    facturas = Factura.objects.select_related('orden', 'cliente', 'empleado').all()
    return render(request, 'gestion/factura_list.html', {'facturas': facturas})


def factura_detail(request, pk):
    factura = get_object_or_404(Factura.objects.select_related('orden', 'cliente', 'empleado'), pk=pk)
    detalles = factura.orden.detalles.select_related('producto').all()
    return render(request, 'gestion/factura_detail.html', {'factura': factura, 'detalles': detalles})
