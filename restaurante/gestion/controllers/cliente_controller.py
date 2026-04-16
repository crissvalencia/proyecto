from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from gestion.models import Cliente
from gestion.helpers.forms import ClienteForm


def cliente_list(request):
    clientes = Cliente.objects.all()
    return render(request, 'gestion/cliente_list.html', {'clientes': clientes})


def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente registrado exitosamente.')
            return redirect('cliente_list')
    else:
        form = ClienteForm()
    return render(request, 'gestion/cliente_form.html', {'form': form, 'titulo': 'Registrar Cliente'})


def cliente_update(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado exitosamente.')
            return redirect('cliente_list')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'gestion/cliente_form.html', {'form': form, 'titulo': 'Editar Cliente'})


def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        if cliente.facturas.exists() or cliente.ordenes.exists():
            messages.error(request, 'No se puede eliminar el cliente porque tiene registros asociados (facturas u órdenes).')
            return redirect('cliente_list')
            
        cliente.delete()
        messages.success(request, 'Cliente eliminado exitosamente.')
        return redirect('cliente_list')
    return render(request, 'gestion/confirm_delete.html', {
        'objeto': cliente, 'tipo': 'cliente', 'cancel_url': 'cliente_list'
    })
