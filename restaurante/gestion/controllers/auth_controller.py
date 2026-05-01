from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from gestion.helpers.forms import CustomUserCreationForm, RecuperarClaveDirectoForm
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

def recuperar_clave_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = RecuperarClaveDirectoForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            nueva_clave = form.cleaned_data['nueva_clave']
            user = User.objects.get(username=username)
            user.set_password(nueva_clave)
            user.save()
            messages.success(request, '¡Tu contraseña ha sido actualizada con éxito! Ya puedes iniciar sesión.')
            return redirect('login')
    else:
        form = RecuperarClaveDirectoForm()
        
    return render(request, 'gestion/recuperar_clave_directo.html', {'form': form})
