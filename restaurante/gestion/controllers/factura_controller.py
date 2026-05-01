from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from gestion.models import Factura
from gestion.helpers.forms import SeleccionarMetodoPagoForm
from decimal import Decimal

def generar_factura_auto(orden, metodo_pago='efectivo',
                         monto_recibido=None,
                         numero_aprobacion=None,
                         numero_transferencia=None):
    """
    Genera la factura al cerrar una orden como 'pagada'.

    Cadena de datos que usa:
        orden.sucursal            → sucursal que emite la factura
        orden.sucursal.empresa    → razón social, NIT, régimen
        orden.sucursal.empresa.porcentaje_impuesto → % impuesto dinámico (no hardcodeado)
    """
    if not orden.cliente or not orden.mesero:
        raise ValueError(
            "No se puede generar la factura: la orden no tiene cliente o mesero asignado."
        )

    if not orden.sucursal:
        raise ValueError(
            "No se puede generar la factura: la orden no tiene sucursal asignada. "
            "Configura primero una empresa y una sucursal en el panel de administración."
        )

    # Porcentaje de impuesto tomado de la empresa (no hardcodeado)
    porcentaje = Decimal(orden.sucursal.empresa.porcentaje_impuesto) / Decimal(100)

    subtotal = orden.total
    impuesto = subtotal * porcentaje
    total    = subtotal + impuesto

    # Calcular vuelto automáticamente si es efectivo
    vuelto = None
    if metodo_pago == 'efectivo' and monto_recibido is not None:
        vuelto = Decimal(monto_recibido) - total

    ultimo = Factura.objects.order_by('-id').first()
    numero = f"FAC-{(ultimo.id + 1 if ultimo else 1):06d}"

    Factura.objects.create(
        orden                = orden,
        cliente              = orden.cliente,
        empleado             = orden.mesero,
        sucursal             = orden.sucursal,
        numero_factura       = numero,
        subtotal             = subtotal,
        impuesto             = impuesto,
        total                = total,
        metodo_pago          = metodo_pago,
        monto_recibido       = monto_recibido if metodo_pago == 'efectivo' else None,
        vuelto               = vuelto,
        numero_aprobacion    = numero_aprobacion if metodo_pago == 'tarjeta' else None,
        numero_transferencia = numero_transferencia if metodo_pago == 'transferencia' else None,
    )


@login_required(login_url='/login/')
def factura_list(request):
    facturas = Factura.objects.select_related(
        'orden', 'cliente', 'empleado', 'sucursal', 'sucursal__empresa'
    ).all()

    q           = request.GET.get('q', '').strip()
    fecha_desde = request.GET.get('fecha_desde', '').strip()
    fecha_hasta = request.GET.get('fecha_hasta', '').strip()
    metodo_pago = request.GET.get('metodo_pago', '').strip()

    if q:
        facturas = facturas.filter(cliente__nombre__icontains=q)
    if fecha_desde:
        facturas = facturas.filter(fecha__date__gte=fecha_desde)
    if fecha_hasta:
        facturas = facturas.filter(fecha__date__lte=fecha_hasta)
    if metodo_pago:
        facturas = facturas.filter(metodo_pago=metodo_pago)

    context = {
        'facturas':           facturas,
        'filtro_q':           q,
        'filtro_fecha_desde': fecha_desde,
        'filtro_fecha_hasta': fecha_hasta,
        'filtro_metodo':      metodo_pago,
        'metodos_pago':       Factura.METODOS_PAGO,
    }
    return render(request, 'gestion/factura_list.html', context)


@login_required(login_url='/login/')
def factura_detail(request, pk):
    factura = get_object_or_404(
        Factura.objects.select_related(
            'orden', 'cliente', 'empleado', 'sucursal', 'sucursal__empresa'
        ),
        pk=pk,
    )
    detalles = factura.orden.detalles.select_related('producto').all()
    return render(request, 'gestion/factura_detail.html', {
        'factura': factura,
        'detalles': detalles,
    })
