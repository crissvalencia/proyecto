from django import forms
import re
from gestion.models import Empleado, Cliente, Mesa, Producto, Reserva, Orden, DetalleOrden, Insumo, Receta, Categoria
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['cedula', 'nombre', 'puesto', 'telefono', 'salario', 'activo']
        widgets = {
            'cedula': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Numero de Cedula',
                'pattern': '[0-9]+',
                'inputmode': 'numeric',
                'oninput': 'this.value = this.value.replace(/[^0-9]/g, "");',
                'maxlength': '10',
                'title': 'Solo se permiten numeros'
            }),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'puesto': forms.Select(attrs={'class': 'form-select'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono (ej: 3123456789)'}),
            'salario': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Salario', 'min': '0', 'step': '0.01'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['nombre'].error_messages.update({'required': 'El nombre del empleado es obligatorio.'})
        self.fields['puesto'].error_messages.update({'required': 'Debe seleccionar un puesto para el empleado.'})
        self.fields['salario'].error_messages.update({'required': 'El salario del empleado es obligatorio.'})
        
        if self.instance and self.instance.pk:
            # Modo edición
            self.fields['cedula'].widget.attrs['readonly'] = 'readonly'
            self.fields['cedula'].widget.attrs['title'] = 'La cédula no se puede modificar'
        else:
            # Modo creación: Quitar el campo 'activo' para que se asigne automáticamente por defecto
            if 'activo' in self.fields:
                del self.fields['activo']

    def clean_cedula(self):
        if self.instance and self.instance.pk:
            return self.instance.cedula
        return self.cleaned_data.get('cedula')

    def clean_salario(self):
        salario = self.cleaned_data.get('salario')
        if salario is not None and salario <= 0:
            raise forms.ValidationError('El salario debe ser un valor mayor a cero.')
        return salario

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        puesto = cleaned_data.get('puesto')
        salario = cleaned_data.get('salario')
        
        if nombre and puesto and salario:
            duplicados = Empleado.objects.filter(nombre=nombre, puesto=puesto, salario=salario)
            if self.instance and self.instance.pk:
                duplicados = duplicados.exclude(pk=self.instance.pk)
            
            if duplicados.exists():
                raise forms.ValidationError("Ya existe un empleado registrado con el mismo nombre, puesto y salario.")
        return cleaned_data


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['cedula', 'nombre', 'telefono', 'email']
        widgets = {
            'cedula': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de cédula',
                'pattern': '[0-9]+',
                'inputmode': 'numeric',
                'oninput': 'this.value = this.value.replace(/[^0-9]/g, "");',
                'title': 'Solo se permiten numeros'
            }),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del cliente'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono (ej: 3123456789)'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['nombre'].error_messages.update({'required': 'El nombre del cliente es obligatorio.'})
        self.fields['telefono'].error_messages.update({'required': 'El teléfono del cliente es obligatorio.'})

        if self.instance and self.instance.pk:
            self.fields['cedula'].widget.attrs['readonly'] = 'readonly'
            self.fields['cedula'].widget.attrs['title'] = 'La cédula no se puede modificar'

    def clean_cedula(self):
        if self.instance and self.instance.pk:
            return self.instance.cedula
        return self.cleaned_data.get('cedula')

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        telefono = cleaned_data.get('telefono')
        
        if nombre and telefono:
            duplicados = Cliente.objects.filter(nombre=nombre, telefono=telefono)
            if self.instance and self.instance.pk:
                duplicados = duplicados.exclude(pk=self.instance.pk)
            
            if duplicados.exists():
                raise forms.ValidationError("Ya existe un cliente registrado con el mismo nombre y teléfono.")
        return cleaned_data


class MesaForm(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = ['numero', 'capacidad', 'disponible']
        widgets = {
            'numero': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Numero de mesa', 'min': '1'}),
            'capacidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Capacidad', 'min': '1'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['numero'].error_messages.update({'required': 'El número de mesa es obligatorio y debe ser único.'})
        self.fields['capacidad'].error_messages.update({'required': 'La capacidad debe ser un número positivo mayor a cero.'})

    def clean_numero(self):
        numero = self.cleaned_data.get('numero')
        if numero:
            duplicados = Mesa.objects.filter(numero=numero)
            if self.instance and self.instance.pk:
                # Excluir la mesa actual en caso de edición
                duplicados = duplicados.exclude(pk=self.instance.pk)
            
            if duplicados.exists():
                raise forms.ValidationError(f"Ya existe una mesa con el número {numero}.")
        return numero

    def clean_capacidad(self):
        capacidad = self.cleaned_data.get('capacidad')
        if capacidad is not None and capacidad <= 0:
            raise forms.ValidationError("La capacidad debe ser un número positivo mayor a cero.")
        return capacidad


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'categoria']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripcion', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio', 'min': '0.01', 'step': '0.01'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la categoría'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción', 'rows': 3}),
        }

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['cliente', 'mesa', 'fecha', 'hora', 'duracion', 'estado', 'num_personas', 'notas']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'mesa': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'duracion': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '13'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'num_personas': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Notas adicionales'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        mesa = cleaned_data.get('mesa')

        if mesa and not mesa.disponible:
            raise forms.ValidationError("La mesa seleccionada no está disponible en este momento. Por favor elija otra mesa o intente más tarde.")

        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')
        duracion = cleaned_data.get('duracion')
        estado = cleaned_data.get('estado')

        import datetime

        if fecha and fecha < datetime.date.today():
            raise forms.ValidationError({'fecha': "No puedes hacer una reserva en una fecha pasada."})

        if duracion and duracion > 3:
            raise forms.ValidationError("La duración máxima de una reserva debe ser de 3 horas o menos.")

        if mesa and fecha and hora and duracion and estado in ['confirmada', 'pendiente']:
            import datetime
            duracion_td = datetime.timedelta(hours=duracion)
            nueva_inicio = datetime.datetime.combine(fecha, hora)
            nueva_fin = nueva_inicio + duracion_td
            
            # Buscar reservas confirmadas el mismo dia para la misma mesa
            reservas_dia = Reserva.objects.filter(mesa=mesa, fecha=fecha, estado='confirmada')
            if self.instance and self.instance.pk:
                reservas_dia = reservas_dia.exclude(pk=self.instance.pk)
                
            for req in reservas_dia:
                req_inicio = datetime.datetime.combine(req.fecha, req.hora)
                req_duracion = datetime.timedelta(hours=req.duracion)
                req_fin = req_inicio + req_duracion
                # Verifica si se solapan en cualquier punto
                if req_inicio < nueva_fin and req_fin > nueva_inicio:
                    raise forms.ValidationError(f"Conflicto de horario: La mesa {mesa.numero} está ocupada por otra reserva de {req.hora.strftime('%I:%M %p')} a {req_fin.strftime('%I:%M %p')}.")
        return cleaned_data


class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ['mesa', 'cliente', 'mesero', 'notas']
        widgets = {
            'mesa': forms.Select(attrs={'class': 'form-select'}),
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'mesero': forms.Select(attrs={'class': 'form-select'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Notas de la orden'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mesero'].queryset = Empleado.objects.filter(activo=True)


class DetalleOrdenForm(forms.ModelForm):
    class Meta:
        model = DetalleOrden
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'value': '1'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.all()


class CambiarEstadoOrdenForm(forms.Form):
    estado = forms.ChoiceField(
        choices=Orden.ESTADOS,
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = ['nombre', 'cantidad', 'unidad_medida', 'stock_minimo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Carne molida'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'unidad_medida': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Kg, gr, unidades'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['producto', 'insumo', 'cantidad_necesaria']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'insumo': forms.Select(attrs={'class': 'form-select'}),
            'cantidad_necesaria': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email',
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions'
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            elif isinstance(field.widget, forms.SelectMultiple):
                field.widget.attrs.update({'class': 'form-control', 'style': 'min-height: 150px;'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name and not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', first_name):
            raise forms.ValidationError("El nombre solo puede contener letras y espacios (sin números).")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name and not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', last_name):
            raise forms.ValidationError("Los apellidos solo pueden contener letras y espacios (sin números).")
        return last_name

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ_]+$', username):
            raise forms.ValidationError("El nombre de usuario solo puede contener letras y guiones bajos (sin números ni espacios).")
        # Validar si ya existe
        if User.objects.filter(username=username).exists():
             raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username
