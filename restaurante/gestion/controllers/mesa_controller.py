from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from gestion.models import Mesa, Reserva, Orden, Sucursal
from gestion.helpers.forms import MesaForm
from gestion.helpers.decorators import admin_required, cajero_or_admin_required   # NUEVO


def _get_sucursal_activa(request):
    try:
        sucursal = request.user.empleado.sucursal
        if sucursal:
            return sucursal
    except Exception:
        pass
    return Sucursal.objects.filter(activo=True).first()


@cajero_or_admin_required          # mesero/cajero necesitan ver las mesas
def mesa_list(request):
    from django.utils import timezone
    from django.db.models import Prefetch
    sucursal = _get_sucursal_activa(request)
    sucursal_id = sucursal.id if sucursal else None
    today = timezone.localdate()
    # prefetch_related evita N+1 queries: el template llama has_reservation_today
    # por cada mesa; sin esto cada llamada dispara una query independiente a BD.
    mesas = (
        Mesa.objects
        .filter(sucursal_id=sucursal_id)
        .prefetch_related(
            Prefetch(
                'reservas',
                queryset=Reserva.objects.filter(
                    fecha=today,
                    estado__in=['confirmada', 'pendiente'],
                ),
                to_attr='_reservas_hoy',
            )
        )
        .order_by('numero')
    )
    return render(request, 'gestion/mesa_list.html', {'mesas': mesas})


@admin_required                    # crear/editar/borrar mesas es config de negocio
def mesa_create(request):
    sucursal = _get_sucursal_activa(request)
    sucursal_id = sucursal.id if sucursal else None
    if not sucursal:
        messages.error(request, 'No hay ninguna sucursal configurada. Crea primero una Empresa y una Sucursal.')
        return redirect('mesa_list')
    if request.method == 'POST':
        form = MesaForm(request.POST, sucursal_id=sucursal_id)
        if form.is_valid():
            mesa = form.save(commit=False)
            mesa.sucursal = sucursal
            mesa.disponible = True
            mesa.save()
            messages.success(request, 'Mesa registrada exitosamente.')
            return redirect('mesa_list')
    else:
        form = MesaForm(sucursal_id=sucursal_id)
    return render(request, 'gestion/mesa_form.html', {'form': form, 'titulo': 'Registrar Mesa'})


@admin_required
def mesa_update(request, pk):
    sucursal = _get_sucursal_activa(request)
    sucursal_id = sucursal.id if sucursal else None
    mesa = get_object_or_404(Mesa, pk=pk, sucursal_id=sucursal_id)
    if request.method == 'POST':
        form = MesaForm(request.POST, instance=mesa, sucursal_id=sucursal_id)
        if form.is_valid():
            updated = form.save(commit=False)
            updated.disponible = mesa.disponible
            updated.save()
            messages.success(request, 'Mesa actualizada exitosamente.')
            return redirect('mesa_list')
    else:
        form = MesaForm(instance=mesa, sucursal_id=sucursal_id)
    return render(request, 'gestion/mesa_form.html', {'form': form, 'titulo': 'Editar Mesa'})


@admin_required
def mesa_delete(request, pk):
    sucursal = _get_sucursal_activa(request)
    sucursal_id = sucursal.id if sucursal else None
    mesa = get_object_or_404(Mesa, pk=pk, sucursal_id=sucursal_id)
    if request.method == 'POST':
        if Reserva.objects.filter(mesa=mesa).exists() or Orden.objects.filter(mesa=mesa).exists():
            messages.error(request, 'No se puede eliminar la mesa porque tiene reservas u órdenes vinculadas.')
            return redirect('mesa_list')
        mesa.delete()
        messages.success(request, 'Mesa eliminada exitosamente.')
        return redirect('mesa_list')
    return render(request, 'gestion/confirm_delete.html', {
        'objeto': mesa, 'tipo': 'mesa', 'cancel_url': 'mesa_list'
    })
