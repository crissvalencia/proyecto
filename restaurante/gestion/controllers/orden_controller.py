import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from gestion.models import Orden, Factura, DetalleOrden, Producto, Sucursal
from gestion.helpers.forms import OrdenForm, DetalleOrdenForm, CambiarEstadoOrdenForm, SeleccionarMetodoPagoForm
from .factura_controller import generar_factura_auto
from gestion.helpers.decorators import cajero_or_admin_required, mesero_or_admin_required, admin_required


def _get_sucursal_activa(request):
    try:
        sucursal = request.user.empleado.sucursal
        if sucursal:
            return sucursal
    except Exception:
        pass
    return Sucursal.objects.filter(activo=True).first()


@mesero_or_admin_required
def orden_list(request):
    qs = Orden.objects.select_related('mesa', 'cliente', 'mesero', 'sucursal').all()

    if not request.user.is_superuser and hasattr(request.user, 'empleado'):
        if request.user.empleado.puesto == 'mesero':
            qs = qs.filter(mesero=request.user.empleado)

    estado = request.GET.get('estado', '').strip()
    if estado:
        qs = qs.filter(estado=estado)

    return render(request, 'gestion/orden_list.html', {
        'ordenes': qs,
        'estado_actual': estado,
        'estados': Orden.ESTADOS,
    })


@mesero_or_admin_required
def orden_create(request):
    sucursal = _get_sucursal_activa(request)

    if not sucursal:
        messages.error(
            request,
            'No hay ninguna sucursal configurada. '
            'Ve al panel de administración y crea primero una Empresa y una Sucursal.'
        )
        return redirect('orden_list')

    if request.method == 'POST':
        form = OrdenForm(request.POST)
        if form.is_valid():
            orden = form.save(commit=False)
            orden.sucursal = sucursal

            # Validar stock antes de guardar
            productos_json = request.POST.get('productos_json', '[]')
            try:
                productos_list = json.loads(productos_json)
                for item in productos_list:
                    producto = Producto.objects.get(id=item['id'])
                    for receta in producto.recetas.all():
                        if receta.insumo.cantidad < receta.cantidad_necesaria * item['cantidad']:
                            messages.error(request, f'Stock insuficiente para preparar: {producto.nombre}')
                            productos = Producto.objects.all()
                            return render(request, 'gestion/orden_form.html', {
                                'form': form, 'titulo': 'Nuevo Pedido', 'productos': productos
                            })
            except Exception as e:
                print("Error validando stock:", e)

            orden.save()
            mesa = orden.mesa
            mesa.disponible = False
            mesa.save()

            try:
                productos_list = json.loads(productos_json)
                for item in productos_list:
                    producto = Producto.objects.get(id=item['id'])
                    DetalleOrden.objects.create(
                        orden           = orden,
                        producto        = producto,
                        cantidad        = item['cantidad'],
                        precio_unitario = producto.precio,
                        subtotal        = item['cantidad'] * producto.precio,
                    )
            except Exception as e:
                print("Error parsing productos JSON:", e)

            orden.calcular_total()

            # Procesar pago al momento de crear el pedido
            metodo_pago = request.POST.get('metodo_pago', 'efectivo')
            monto_recibido = request.POST.get('monto_recibido', '').strip()
            numero_aprobacion = request.POST.get('numero_aprobacion', '').strip()
            numero_transferencia = request.POST.get('numero_transferencia', '').strip()

            pago_valido = True
            if metodo_pago == 'efectivo':
                if not monto_recibido:
                    messages.error(request, 'Ingresa el monto recibido para pago en efectivo.')
                    pago_valido = False
                else:
                    from decimal import Decimal
                    try:
                        monto_decimal = Decimal(monto_recibido)
                        porcentaje = Decimal(sucursal.empresa.porcentaje_impuesto) / Decimal(100)
                        total_con_impuesto = orden.total + (orden.total * porcentaje)
                        if monto_decimal < total_con_impuesto:
                            messages.error(request, 'El monto recibido es menor al total de la factura.')
                            pago_valido = False
                    except Exception:
                        messages.error(request, 'El monto recibido no es válido.')
                        pago_valido = False
            elif metodo_pago == 'tarjeta' and not numero_aprobacion:
                messages.error(request, 'Ingresa el número de aprobación del datáfono.')
                pago_valido = False
            elif metodo_pago == 'transferencia' and not numero_transferencia:
                messages.error(request, 'Ingresa el número de referencia de la transferencia.')
                pago_valido = False

            if pago_valido:
                try:
                    generar_factura_auto(
                        orden,
                        metodo_pago=metodo_pago,
                        monto_recibido=monto_recibido or None,
                        numero_aprobacion=numero_aprobacion or None,
                        numero_transferencia=numero_transferencia or None,
                    )
                    messages.info(request, 'Factura generada automáticamente.')
                except Exception as e:
                    messages.warning(request, f'Pedido creado, pero no se pudo generar la factura: {e}')

            messages.success(request, 'Pedido creado exitosamente.')
            return redirect('orden_list')
    else:
        form = OrdenForm()

    productos = Producto.objects.all()
    return render(request, 'gestion/orden_form.html', {
        'form': form, 'titulo': 'Nuevo Pedido', 'productos': productos
    })


@mesero_or_admin_required
def orden_detail(request, pk):
    orden = get_object_or_404(
        Orden.objects.select_related('mesa', 'cliente', 'mesero', 'sucursal'),
        pk=pk,
    )
    detalles     = orden.detalles.select_related('producto').all()
    detalle_form = DetalleOrdenForm()
    estado_form  = CambiarEstadoOrdenForm(estado_actual=orden.estado)
    pago_form    = SeleccionarMetodoPagoForm()
    return render(request, 'gestion/orden_detail.html', {
        'orden':        orden,
        'detalles':     detalles,
        'detalle_form': detalle_form,
        'estado_form':  estado_form,
        'pago_form':    pago_form,
    })


@mesero_or_admin_required
def orden_agregar_detalle(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    if request.method == 'POST':
        form = DetalleOrdenForm(request.POST)
        if form.is_valid():
            detalle       = form.save(commit=False)
            detalle.orden = orden

            for receta in detalle.producto.recetas.all():
                if receta.insumo.cantidad < receta.cantidad_necesaria * detalle.cantidad:
                    messages.error(request, f'Stock insuficiente para: {detalle.producto.nombre}')
                    return redirect('orden_detail', pk=pk)

            try:
                detalle.save()
                orden.calcular_total()
                messages.success(request, 'Producto agregado a la orden.')
            except ValueError as e:
                messages.error(request, str(e))
    return redirect('orden_detail', pk=pk)


@cajero_or_admin_required
def orden_cambiar_estado(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    if request.method == 'POST':
        form = CambiarEstadoOrdenForm(request.POST, estado_actual=orden.estado)
        if form.is_valid():
            TRANSICIONES_VALIDAS = {
                'pendiente':      ['en_preparacion', 'cancelada'],
                'en_preparacion': ['lista',          'cancelada'],
                'lista':          ['pagada',         'cancelada'],
                'pagada':         [],
                'cancelada':      [],
            }

            if orden.estado in ('pagada', 'cancelada'):
                messages.error(request, 'No se puede modificar una orden ya cerrada.')
                return redirect('orden_detail', pk=pk)

            nuevo_estado = form.cleaned_data['estado']

            if nuevo_estado not in TRANSICIONES_VALIDAS.get(orden.estado, []):
                messages.error(
                    request,
                    f'Transición no permitida: {orden.get_estado_display()} → '
                    f'{dict(Orden.ESTADOS).get(nuevo_estado, nuevo_estado)}.'
                )
                return redirect('orden_detail', pk=pk)

            orden.estado = nuevo_estado
            orden.save()

            messages.success(request, f'Estado actualizado a: {orden.get_estado_display()}')

            if nuevo_estado == 'pagada':
                try:
                    orden.factura
                except Factura.DoesNotExist:
                    pago_form = SeleccionarMetodoPagoForm(request.POST)
                    metodo    = pago_form.cleaned_data['metodo_pago'] if pago_form.is_valid() else 'efectivo'

                    monto_recibido       = request.POST.get('monto_recibido')
                    numero_aprobacion    = request.POST.get('numero_aprobacion')
                    numero_transferencia = request.POST.get('numero_transferencia')

                    if metodo == 'efectivo':
                        if not monto_recibido:
                            messages.error(request, 'Ingresa el monto recibido para pago en efectivo.')
                            orden.estado = 'lista'
                            orden.save()
                            return redirect('orden_detail', pk=pk)

                        from decimal import Decimal
                        porcentaje = Decimal(orden.sucursal.empresa.porcentaje_impuesto) / Decimal(100)
                        total_con_impuesto = orden.total + (orden.total * porcentaje)

                        if Decimal(monto_recibido) < total_con_impuesto:
                            messages.error(request, 'El monto recibido es menor al total de la factura.')
                            orden.estado = 'lista'
                            orden.save()
                            return redirect('orden_detail', pk=pk)

                    elif metodo == 'tarjeta' and not numero_aprobacion:
                        messages.error(request, 'Ingresa el número de aprobación del datáfono.')
                        orden.estado = 'lista'
                        orden.save()
                        return redirect('orden_detail', pk=pk)

                    elif metodo == 'transferencia' and not numero_transferencia:
                        messages.error(request, 'Ingresa el número de referencia de la transferencia.')
                        orden.estado = 'lista'
                        orden.save()
                        return redirect('orden_detail', pk=pk)

                    try:
                        generar_factura_auto(
                            orden,
                            metodo_pago=metodo,
                            monto_recibido=monto_recibido,
                            numero_aprobacion=numero_aprobacion,
                            numero_transferencia=numero_transferencia
                        )
                        messages.info(request, 'Factura generada automáticamente.')
                    except ValueError as e:
                        messages.error(request, str(e))

            if nuevo_estado in ['pagada', 'cancelada']:
                orden.mesa.disponible = True
                orden.mesa.save()
            elif nuevo_estado in ['pendiente', 'en_preparacion', 'lista']:
                orden.mesa.disponible = False
                orden.mesa.save()

    return redirect('orden_detail', pk=pk)


@admin_required
def orden_delete(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    if request.method == 'POST':
        mesa = orden.mesa
        orden.delete()
        if mesa:
            mesa.disponible = True
            mesa.save()
        messages.success(request, 'Orden eliminada exitosamente.')
        return redirect('orden_list')
    return render(request, 'gestion/confirm_delete.html', {
        'objeto': orden, 'tipo': 'orden', 'cancel_url': 'orden_list'
    })