from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError
from gestion.models import Reserva
from gestion.helpers.forms import ReservaForm
from gestion.helpers.decorators import cajero_or_admin_required


@cajero_or_admin_required
def reserva_list(request):
    reservas = Reserva.objects.select_related('cliente', 'mesa').all()

    estado = request.GET.get('estado', '').strip()
    fecha  = request.GET.get('fecha', '').strip()
    q      = request.GET.get('q', '').strip()

    if estado:
        reservas = reservas.filter(estado=estado)
    if fecha:
        reservas = reservas.filter(fecha=fecha)
    if q:
        reservas = reservas.filter(cliente__nombre__icontains=q)

    context = {
        'reservas': reservas,
        'filtro_estado': estado,
        'filtro_fecha':  fecha,
        'filtro_q':      q,
        'estados':       Reserva.ESTADOS,
    }
    return render(request, 'gestion/reserva_list.html', context)


@cajero_or_admin_required
def reserva_create(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Reserva registrada exitosamente.')
                return redirect('reserva_list')
            except ValidationError as e:
                messages.error(request, str(e))
    else:
        form = ReservaForm()
    return render(request, 'gestion/reserva_form.html', {'form': form, 'titulo': 'Nueva Reserva'})


@cajero_or_admin_required
def reserva_update(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Reserva actualizada exitosamente.')
                return redirect('reserva_list')
            except ValidationError as e:
                messages.error(request, str(e))
    else:
        form = ReservaForm(instance=reserva)
    return render(request, 'gestion/reserva_form.html', {'form': form, 'titulo': 'Editar Reserva'})


@cajero_or_admin_required
def reserva_delete(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == 'POST':
        reserva.delete()
        messages.success(request, 'Reserva eliminada exitosamente.')
        return redirect('reserva_list')
    return render(request, 'gestion/confirm_delete.html', {
        'objeto': reserva, 'tipo': 'reserva', 'cancel_url': 'reserva_list'
    })
