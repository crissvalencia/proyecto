from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from gestion.models import Receta, Producto
from gestion.helpers.forms import RecetaForm
from gestion.helpers.decorators import admin_required


@admin_required
def receta_list(request):
    """Lista todas las recetas agrupadas por producto."""
    productos_con_recetas = Producto.objects.prefetch_related(
        'recetas__insumo'
    ).filter(recetas__isnull=False).distinct().order_by('nombre')

    productos_sin_recetas = Producto.objects.filter(
        recetas__isnull=True
    ).order_by('nombre')

    return render(request, 'gestion/receta_list.html', {
        'productos_con_recetas': productos_con_recetas,
        'productos_sin_recetas': productos_sin_recetas,
    })


@admin_required
def receta_create(request):
    """Crea un nuevo ítem de receta (producto + insumo + cantidad)."""
    producto_id = request.GET.get('producto')
    initial = {}
    if producto_id:
        initial['producto'] = producto_id

    if request.method == 'POST':
        form = RecetaForm(request.POST)
        if form.is_valid():
            receta = form.save()
            messages.success(
                request,
                f'Ingrediente "{receta.insumo.nombre}" agregado a la receta de "{receta.producto.nombre}".'
            )
            return redirect('receta_list')
    else:
        form = RecetaForm(initial=initial)

    return render(request, 'gestion/receta_form.html', {
        'form': form,
        'titulo': 'Agregar Ingrediente a Receta',
    })


@admin_required
def receta_update(request, pk):
    """Edita la cantidad necesaria de un ingrediente en una receta."""
    receta = get_object_or_404(Receta, pk=pk)

    if request.method == 'POST':
        form = RecetaForm(request.POST, instance=receta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ingrediente de receta actualizado correctamente.')
            return redirect('receta_list')
    else:
        form = RecetaForm(instance=receta)

    return render(request, 'gestion/receta_form.html', {
        'form': form,
        'titulo': f'Editar Ingrediente: {receta.insumo.nombre} en {receta.producto.nombre}',
        'receta': receta,
    })


@admin_required
def receta_delete(request, pk):
    """Elimina un ingrediente de una receta."""
    receta = get_object_or_404(Receta, pk=pk)

    if request.method == 'POST':
        nombre_producto = receta.producto.nombre
        nombre_insumo = receta.insumo.nombre
        receta.delete()
        messages.success(
            request,
            f'Ingrediente "{nombre_insumo}" eliminado de la receta de "{nombre_producto}".'
        )
        return redirect('receta_list')

    return render(request, 'gestion/confirm_delete.html', {
        'objeto': receta,
        'tipo': 'ingrediente de receta',
        'cancel_url': 'receta_list',
    })
