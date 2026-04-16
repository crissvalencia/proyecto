import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from gestion.models import Orden, Factura, DetalleOrden, Producto
from gestion.helpers.forms import OrdenForm, DetalleOrdenForm, CambiarEstadoOrdenForm
from .factura_controller import generar_factura_auto


def orden_list(request):
    ordenes = Orden.objects.select_related('mesa', 'cliente', 'mesero').all()
    return render(request, 'gestion/orden_list.html', {'ordenes': ordenes})


def orden_create(request):
    if request.method == 'POST':
        form = OrdenForm(request.POST)
        if form.is_valid():
            orden = form.save(commit=False)

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
                            return render(request, 'gestion/orden_form.html', {'form': form, 'titulo': 'Nuevo Pedido', 'productos': productos})
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
                        orden=orden,
                        producto=producto,
                        cantidad=item['cantidad'],
                        precio_unitario=producto.precio,
                        subtotal=item['cantidad'] * producto.precio
                    )
            except Exception as e:
                print("Error parsing productos JSON:", e)

            orden.calcular_total()
            messages.success(request, 'Pedido creado exitosamente.')
            return redirect('orden_list')
    else:
        form = OrdenForm()

    productos = Producto.objects.all()
    return render(request, 'gestion/orden_form.html', {'form': form, 'titulo': 'Nuevo Pedido', 'productos': productos})


def orden_detail(request, pk):
    orden = get_object_or_404(Orden.objects.select_related('mesa', 'cliente', 'mesero'), pk=pk)
    detalles = orden.detalles.select_related('producto').all()
    detalle_form = DetalleOrdenForm()
    estado_form = CambiarEstadoOrdenForm(initial={'estado': orden.estado})
    return render(request, 'gestion/orden_detail.html', {
        'orden': orden, 'detalles': detalles,
        'detalle_form': detalle_form, 'estado_form': estado_form,
    })


def orden_agregar_detalle(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    if request.method == 'POST':
        form = DetalleOrdenForm(request.POST)
        if form.is_valid():
            detalle = form.save(commit=False)
            detalle.orden = orden

            # Validar stock antes de guardar
            for receta in detalle.producto.recetas.all():
                if receta.insumo.cantidad < receta.cantidad_necesaria * detalle.cantidad:
                    messages.error(request, f'Stock insuficiente para: {detalle.producto.nombre}')
                    return redirect('orden_detail', pk=pk)

            detalle.save()
            orden.calcular_total()
            messages.success(request, 'Producto agregado a la orden.')
    return redirect('orden_detail', pk=pk)

def orden_cambiar_estado(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    if request.method == 'POST':
        form = CambiarEstadoOrdenForm(request.POST)
        if form.is_valid():
            nuevo_estado = form.cleaned_data['estado']
            orden.estado = nuevo_estado
            orden.save()
            
            if nuevo_estado in ['entregada', 'cancelada']:
                mesa = orden.mesa
                mesa.disponible = True
                mesa.save()
            elif nuevo_estado in ['pendiente', 'en_preparacion', 'lista']:
                mesa = orden.mesa
                mesa.disponible = False
                mesa.save()
                
            messages.success(request, f'Estado de la orden actualizado a: {orden.get_estado_display()}')
            if nuevo_estado == 'entregada':
                try:
                    orden.factura
                except Factura.DoesNotExist:
                    generar_factura_auto(orden)
                    messages.info(request, 'Factura generada automaticamente.')
    return redirect('orden_detail', pk=pk)


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
