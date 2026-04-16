from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from gestion.models import Empleado
from gestion.helpers.forms import EmpleadoForm
from gestion.helpers.decorators import admin_required


from django.contrib.auth.models import User

@admin_required(login_url='dashboard')
def empleado_list(request):
    empleados = Empleado.objects.all()
    return render(request, 'gestion/empleado_list.html', {'empleados': empleados})


@admin_required(login_url='dashboard')
def empleado_create(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            empleado = form.save(commit=False)
            user, created = User.objects.get_or_create(username=empleado.cedula)
            if created:
                user.set_password(empleado.cedula)
                user.save()
            empleado.usuario = user
            empleado.save()
            messages.success(request, 'Empleado registrado exitosamente. Su usuario y contraseña son su número de cédula.')
            return redirect('empleado_list')
    else:
        form = EmpleadoForm()
    return render(request, 'gestion/empleado_form.html', {'form': form, 'titulo': 'Registrar Empleado'})


@admin_required(login_url='dashboard')
def empleado_update(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            empleado = form.save()
            if empleado.usuario:
                empleado.usuario.is_active = empleado.activo
                empleado.usuario.save()
            messages.success(request, 'Empleado actualizado exitosamente.')
            return redirect('empleado_list')
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, 'gestion/empleado_form.html', {'form': form, 'titulo': 'Editar Empleado'})


@admin_required(login_url='dashboard')
def empleado_delete(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        usuario = empleado.usuario
        empleado.delete()
        if usuario:
            usuario.delete()
        messages.success(request, 'Empleado eliminado exitosamente.')
        return redirect('empleado_list')
    return render(request, 'gestion/confirm_delete.html', {
        'objeto': empleado, 'tipo': 'empleado', 'cancel_url': 'empleado_list'
    })
