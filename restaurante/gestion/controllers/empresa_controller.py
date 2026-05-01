from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from gestion.models import Empresa, Sucursal
from gestion.helpers.forms import EmpresaForm, SucursalForm
from gestion.helpers.decorators import admin_required

# --- CRUD EMPRESA ---

@admin_required
def empresa_list(request):
    empresas = Empresa.objects.all()
    return render(request, 'gestion/empresa_list.html', {'empresas': empresas})

@admin_required
def empresa_create(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empresa creada exitosamente.')
            return redirect('empresa_list')
    else:
        form = EmpresaForm()
    return render(request, 'gestion/empresa_form.html', {'form': form, 'titulo': 'Registrar Empresa'})

@admin_required
def empresa_update(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    if request.method == 'POST':
        form = EmpresaForm(request.POST, instance=empresa)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empresa actualizada exitosamente.')
            return redirect('empresa_list')
    else:
        form = EmpresaForm(instance=empresa)
    return render(request, 'gestion/empresa_form.html', {'form': form, 'titulo': 'Editar Empresa'})

@admin_required
def empresa_delete(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    if request.method == 'POST':
        empresa.delete()
        messages.success(request, 'Empresa eliminada exitosamente.')
        return redirect('empresa_list')
    return render(request, 'gestion/confirm_delete.html', {
        'objeto': empresa, 'tipo': 'empresa', 'cancel_url': 'empresa_list'
    })


# --- CRUD SUCURSAL ---

@admin_required
def sucursal_list(request, empresa_id):
    empresa = get_object_or_404(Empresa, pk=empresa_id)
    sucursales = empresa.sucursales.all()
    return render(request, 'gestion/sucursal_list.html', {'empresa': empresa, 'sucursales': sucursales})

@admin_required
def sucursal_create(request, empresa_id):
    empresa = get_object_or_404(Empresa, pk=empresa_id)
    if request.method == 'POST':
        form = SucursalForm(request.POST)
        if form.is_valid():
            sucursal = form.save(commit=False)
            sucursal.empresa = empresa
            sucursal.save()
            messages.success(request, 'Sucursal creada exitosamente.')
            return redirect('sucursal_list', empresa_id=empresa.id)
    else:
        form = SucursalForm()
    return render(request, 'gestion/sucursal_form.html', {'form': form, 'titulo': f'Registrar Sucursal para {empresa.razon_social}'})

@admin_required
def sucursal_update(request, empresa_id, pk):
    empresa = get_object_or_404(Empresa, pk=empresa_id)
    sucursal = get_object_or_404(Sucursal, pk=pk, empresa=empresa)
    if request.method == 'POST':
        form = SucursalForm(request.POST, instance=sucursal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sucursal actualizada exitosamente.')
            return redirect('sucursal_list', empresa_id=empresa.id)
    else:
        form = SucursalForm(instance=sucursal)
    return render(request, 'gestion/sucursal_form.html', {'form': form, 'titulo': 'Editar Sucursal'})

@admin_required
def sucursal_delete(request, empresa_id, pk):
    empresa = get_object_or_404(Empresa, pk=empresa_id)
    sucursal = get_object_or_404(Sucursal, pk=pk, empresa=empresa)
    if request.method == 'POST':
        sucursal.delete()
        messages.success(request, 'Sucursal eliminada exitosamente.')
        return redirect('sucursal_list', empresa_id=empresa.id)
    return render(request, 'gestion/confirm_delete.html', {
        'objeto': sucursal, 'tipo': 'sucursal', 'cancel_url': 'sucursal_list', 'cancel_args': empresa.id
    })
