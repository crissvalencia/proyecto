from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from gestion.models import Producto, Categoria
from gestion.helpers.forms import ProductoForm, CategoriaForm


def producto_list(request):
    productos = Producto.objects.select_related('categoria').all()
    return render(request, 'gestion/producto_list.html', {'productos': productos})


def producto_create(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto registrado exitosamente.')
            return redirect('producto_list')
    else:
        form = ProductoForm()
    return render(request, 'gestion/producto_form.html', {'form': form, 'titulo': 'Registrar Producto'})


def producto_update(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente.')
            return redirect('producto_list')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'gestion/producto_form.html', {'form': form, 'titulo': 'Editar Producto'})


def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
        return redirect('producto_list')
    return render(request, 'gestion/confirm_delete.html', {
        'objeto': producto, 'tipo': 'producto', 'cancel_url': 'producto_list'
    })


def categoria_list(request):
    categorias = Categoria.objects.prefetch_related('productos').all()
    return render(request, 'gestion/categoria_list.html', {'categorias': categorias})


def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente.')
            return redirect('categoria_list')
    else:
        form = CategoriaForm()
    return render(request, 'gestion/categoria_form.html', {'form': form, 'titulo': 'Nueva Categoría'})


def categoria_update(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada exitosamente.')
            return redirect('categoria_list')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'gestion/categoria_form.html', {'form': form, 'titulo': 'Editar Categoría'})


def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoría eliminada exitosamente.')
        return redirect('categoria_list')
    return render(request, 'gestion/confirm_delete.html', {
        'objeto': categoria, 'tipo': 'categoría', 'cancel_url': 'categoria_list'
    })