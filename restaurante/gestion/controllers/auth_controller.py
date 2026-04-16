from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from gestion.helpers.forms import CustomUserCreationForm
from gestion.helpers.decorators import admin_required

@admin_required(login_url='dashboard')
def crear_usuario_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            nuevo_usuario = form.save()
            messages.success(request, f'¡El usuario {nuevo_usuario.username} se creó exitosamente!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'gestion/crear_usuario.html', {'form': form})

@admin_required(login_url='dashboard')
def usuario_list_view(request):
    usuarios = User.objects.all().order_by('-date_joined')
    return render(request, 'gestion/usuario_list.html', {'usuarios': usuarios})
