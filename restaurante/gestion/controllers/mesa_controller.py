from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from gestion.models import Mesa, Reserva, Orden
from gestion.helpers.forms import MesaForm


def mesa_list(request):
    mesas = Mesa.objects.all()
    return render(request, 'gestion/mesa_list.html', {'mesas': mesas})


def mesa_create(request):
    if request.method == 'POST':
        form = MesaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mesa registrada exitosamente.')
            return redirect('mesa_list')
    else:
        form = MesaForm()
    return render(request, 'gestion/mesa_form.html', {'form': form, 'titulo': 'Registrar Mesa'})


def mesa_update(request, pk):
    mesa = get_object_or_404(Mesa, pk=pk)
    if request.method == 'POST':
        form = MesaForm(request.POST, instance=mesa)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mesa actualizada exitosamente.')
            return redirect('mesa_list')
    else:
        form = MesaForm(instance=mesa)
    return render(request, 'gestion/mesa_form.html', {'form': form, 'titulo': 'Editar Mesa'})


def mesa_delete(request, pk):
    mesa = get_object_or_404(Mesa, pk=pk)
    if request.method == 'POST':
        # Verificar si la mesa tiene reservas u órdenes vinculadas
        if Reserva.objects.filter(mesa=mesa).exists() or Orden.objects.filter(mesa=mesa).exists():
            messages.error(request, 'No se puede eliminar la mesa porque tiene reservas u órdenes vinculadas.')
            return redirect('mesa_list')
            
        mesa.delete()
        messages.success(request, 'Mesa eliminada exitosamente.')
        return redirect('mesa_list')
    return render(request, 'gestion/confirm_delete.html', {
        'objeto': mesa, 'tipo': 'mesa', 'cancel_url': 'mesa_list'
    })
