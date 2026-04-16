from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from gestion.models import Insumo
from gestion.helpers.forms import InsumoForm


def insumo_list(request):
    insumos = Insumo.objects.all()
    return render(request, 'gestion/insumo_list.html', {'insumos': insumos})


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


def insumo_delete(request, pk):
    insumo = get_object_or_404(Insumo, pk=pk)
    if request.method == 'POST':
        insumo.delete()
        messages.success(request, 'Insumo eliminado exitosamente.')
        return redirect('insumo_list')
    return render(request, 'gestion/confirm_delete.html', {
        'objeto': insumo, 'tipo': 'insumo', 'cancel_url': 'insumo_list'
    })
