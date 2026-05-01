from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from gestion.models import Insumo
from gestion.helpers.forms import InsumoForm
from gestion.helpers.decorators import admin_required   # NUEVO


@admin_required
def insumo_list(request):
    insumos = Insumo.objects.all()

    q          = request.GET.get('q', '').strip()
    stock_bajo = request.GET.get('stock_bajo', '').strip()

    if q:
        insumos = insumos.filter(nombre__icontains=q)
    if stock_bajo:
        from django.db.models import F
        insumos = insumos.filter(cantidad__lte=F('stock_minimo'))

    context = {
        'insumos':          insumos,
        'filtro_q':         q,
        'filtro_stock_bajo': stock_bajo,
    }
    return render(request, 'gestion/insumo_list.html', context)


@admin_required
def insumo_create(request):
    if request.method == 'POST':
        form = InsumoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Insumo creado exitosamente.')
            return redirect('insumo_list')
    else:
        form = InsumoForm()
    return render(request, 'gestion/insumo_form.html', {'form': form, 'titulo': 'Nuevo Insumo'})


@admin_required
def insumo_update(request, pk):
    insumo = get_object_or_404(Insumo, pk=pk)
    if request.method == 'POST':
        form = InsumoForm(request.POST, instance=insumo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Insumo actualizado exitosamente.')
            return redirect('insumo_list')
    else:
        form = InsumoForm(instance=insumo)
    return render(request, 'gestion/insumo_form.html', {'form': form, 'titulo': 'Editar Insumo'})


@admin_required
def insumo_delete(request, pk):
    insumo = get_object_or_404(Insumo, pk=pk)
    if request.method == 'POST':
        insumo.delete()
        messages.success(request, 'Insumo eliminado exitosamente.')
        return redirect('insumo_list')
    return render(request, 'gestion/confirm_delete.html', {
        'objeto': insumo, 'tipo': 'insumo', 'cancel_url': 'insumo_list'
    })
