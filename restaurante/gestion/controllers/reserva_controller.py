from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from gestion.models import Reserva
from gestion.helpers.forms import ReservaForm
from datetime import datetime, timedelta 

def reserva_list(request):
    reservas = Reserva.objects.select_related('cliente', 'mesa').all()
    return render(request, 'gestion/reserva_list.html', {'reservas': reservas})




def reserva_create(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            
            hora_inicio = datetime.combine(reserva.fecha, reserva.hora)
            hora_fin = hora_inicio + timedelta(hours=2)
            hora_limite_inicio = (hora_inicio - timedelta(hours=2)).time()

            conflicto = Reserva.objects.filter(
                mesa=reserva.mesa,
                fecha=reserva.fecha,
                estado='confirmada'
            ).filter(
                hora__gte=hora_limite_inicio,
                hora__lt=hora_fin.time()
            ).exists()

            if conflicto:
                messages.error(request, 'La mesa no está disponible en ese horario.')
            else:
                reserva.save()
                messages.success(request, 'Reserva registrada exitosamente.')
                return redirect('reserva_list')
    else:
        form = ReservaForm()
    return render(request, 'gestion/reserva_form.html', {'form': form, 'titulo': 'Nueva Reserva'})

def reserva_update(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    old_mesa = reserva.mesa
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            nueva_reserva = form.save(commit=False)

            hora_inicio = datetime.combine(nueva_reserva.fecha, nueva_reserva.hora)
            hora_fin = hora_inicio + timedelta(hours=2)
            hora_limite_inicio = (hora_inicio - timedelta(hours=2)).time()

            conflicto = Reserva.objects.filter(
                mesa=nueva_reserva.mesa,
                fecha=nueva_reserva.fecha,
                estado='confirmada'
            ).exclude(pk=pk).filter(
                hora__gte=hora_limite_inicio,
                hora__lt=hora_fin.time()
            ).exists()

            if conflicto:
                messages.error(request, 'La mesa no está disponible en ese horario.')
            else:
                nueva_reserva.save()
                messages.success(request, 'Reserva actualizada exitosamente.')
                return redirect('reserva_list')
    else:
        form = ReservaForm(instance=reserva)
    return render(request, 'gestion/reserva_form.html', {'form': form, 'titulo': 'Editar Reserva'})


def reserva_delete(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == 'POST':
        reserva.delete()
        messages.success(request, 'Reserva eliminada exitosamente.')
        return redirect('reserva_list')
    return render(request, 'gestion/confirm_delete.html', {
        'objeto': reserva, 'tipo': 'reserva', 'cancel_url': 'reserva_list'
    })
