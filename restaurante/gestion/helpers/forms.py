from django import forms
import re
from gestion.models import Empleado, Cliente, Mesa, Producto, Reserva, Orden, DetalleOrden, Insumo, Receta, Categoria, Empresa, Sucursal
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['tipo_documento', 'numero_documento', 'nombre', 'apellido', 'puesto', 'sucursal', 'telefono', 'salario', 'activo']
        widgets = {
            'tipo_documento': forms.Select(attrs={
                'class': 'form-select',
            }),
            'numero_documento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de documento',
                'title': 'Ingrese el número de documento',
            }),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'puesto': forms.Select(attrs={'class': 'form-select'}),
            'sucursal': forms.Select(attrs={'class': 'form-select'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono (ej: 3123456789)'}),
            'salario': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Salario', 'min': '0', 'step': '0.01'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['nombre'].error_messages.update({'required': 'El nombre del empleado es obligatorio.'})
        self.fields['apellido'].error_messages.update({'required': 'El apellido del empleado es obligatorio.'})
        self.fields['puesto'].error_messages.update({'required': 'Debe seleccionar un puesto para el empleado.'})
        self.fields['salario'].error_messages.update({'required': 'El salario del empleado es obligatorio.'})

        if self.instance and self.instance.pk:
            # Modo edición: bloquear documento
            self.fields['tipo_documento'].widget.attrs['disabled'] = 'disabled'
            self.fields['numero_documento'].widget.attrs['readonly'] = 'readonly'
            self.fields['numero_documento'].widget.attrs['title'] = 'El documento no se puede modificar'
        else:
            if 'activo' in self.fields:
                del self.fields['activo']

    def clean_tipo_documento(self):
        if self.instance and self.instance.pk:
            return self.instance.tipo_documento
        return self.cleaned_data.get('tipo_documento')

    def clean_numero_documento(self):
        if self.instance and self.instance.pk:
            return self.instance.numero_documento
        return self.cleaned_data.get('numero_documento')

    def clean_salario(self):
        salario = self.cleaned_data.get('salario')
        if salario is not None and salario <= 0:
            raise forms.ValidationError('El salario debe ser un valor mayor a cero.')
        return salario

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo_documento')
        numero = cleaned_data.get('numero_documento')
        nombre = cleaned_data.get('nombre')
        puesto = cleaned_data.get('puesto')
        salario = cleaned_data.get('salario')

        if tipo and numero:
            if tipo == 'CC':
                if not numero.isdigit():
                    self.add_error('numero_documento', 'La Cédula de Ciudadanía solo puede contener números.')
                elif len(numero) > 10:
                    self.add_error('numero_documento', 'La Cédula de Ciudadanía no puede superar 10 dígitos.')
            elif tipo in ('PPT', 'PEP', 'CE', 'PA'):
                if len(numero) > 20:
                    self.add_error('numero_documento', 'El documento no puede superar 20 caracteres.')

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
        fields = ['tipo_documento', 'numero_documento', 'nombre', 'telefono', 'email']
        widgets = {
            'tipo_documento': forms.Select(attrs={
                'class': 'form-select',
            }),
            'numero_documento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de documento',
                'title': 'Ingrese el número de documento',
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
            self.fields['tipo_documento'].widget.attrs['disabled'] = 'disabled'
            self.fields['numero_documento'].widget.attrs['readonly'] = 'readonly'
            self.fields['numero_documento'].widget.attrs['title'] = 'El documento no se puede modificar'

    def clean_tipo_documento(self):
        if self.instance and self.instance.pk:
            return self.instance.tipo_documento
        return self.cleaned_data.get('tipo_documento')

    def clean_numero_documento(self):
        if self.instance and self.instance.pk:
            return self.instance.numero_documento
        return self.cleaned_data.get('numero_documento')

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '').strip()
        if not telefono:
            raise forms.ValidationError('El teléfono del cliente es obligatorio.')
        if not re.match(r'^3\d{9}$', telefono):
            raise forms.ValidationError(
                'El teléfono debe tener 10 dígitos y comenzar por 3 (ej: 3123456789).'
            )
        return telefono

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
        fields = ['numero', 'capacidad']
        widgets = {
            'numero': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Numero de mesa', 'min': '1'}),
            'capacidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Capacidad', 'min': '1'}),
        }

    def __init__(self, *args, sucursal_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.sucursal_id = sucursal_id
        self.fields['numero'].error_messages.update({'required': 'El número de mesa es obligatorio y debe ser único.'})
        self.fields['capacidad'].error_messages.update({'required': 'La capacidad debe ser un número positivo mayor a cero.'})

    def clean_numero(self):
        numero = self.cleaned_data.get('numero')
        if numero:
            duplicados = Mesa.objects.filter(numero=numero, sucursal_id=self.sucursal_id)
            if self.instance and self.instance.pk:
                duplicados = duplicados.exclude(pk=self.instance.pk)
            if duplicados.exists():
                raise forms.ValidationError(f"Ya existe una mesa con el número {numero} en esta sucursal.")
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
            raise forms.ValidationError(
                "La mesa seleccionada no está disponible en este momento. "
                "Por favor elija otra mesa o intente más tarde."
            )

        fecha = cleaned_data.get('fecha')
        import datetime
        if fecha and fecha < datetime.date.today():
            raise forms.ValidationError({'fecha': "No puedes hacer una reserva en una fecha pasada."})

        duracion = cleaned_data.get('duracion')
        if duracion and duracion > 3:
            raise forms.ValidationError("La duración máxima de una reserva debe ser de 3 horas o menos.")

        # La validación de solapamiento ya la ejecuta el modelo en full_clean().
        # No se duplica aquí para evitar errores dobles al usuario.

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


TRANSICIONES_VALIDAS = {
    'pendiente':      ['en_preparacion', 'cancelada'],
    'en_preparacion': ['lista',          'cancelada'],
    'lista':          ['pagada',         'cancelada'],
    'pagada':         [],
    'cancelada':      [],
}

class CambiarEstadoOrdenForm(forms.Form):
    estado = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, estado_actual=None, **kwargs):
        super().__init__(*args, **kwargs)
        estados_dict = dict(Orden.ESTADOS)
        if estado_actual and estado_actual in TRANSICIONES_VALIDAS:
            opciones = TRANSICIONES_VALIDAS[estado_actual]
            self.fields['estado'].choices = [
                (e, estados_dict[e]) for e in opciones
            ]
        else:
            self.fields['estado'].choices = Orden.ESTADOS


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

class SeleccionarMetodoPagoForm(forms.Form):
    metodo_pago = forms.ChoiceField(
        choices=[
            ('efectivo',       'Efectivo'),
            ('tarjeta',        'Tarjeta'),
            ('transferencia',  'Transferencia'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Método de pago',
        initial='efectivo',
    )


class RecuperarClaveDirectoForm(forms.Form):
    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre de usuario'})
    )
    numero_documento = forms.CharField(
        label='Número de documento',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu número de documento'})
    )
    nueva_clave = forms.CharField(
        label='Nueva Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Escribe tu nueva clave'})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        numero_documento = cleaned_data.get('numero_documento')

        if username and numero_documento:
            try:
                user = User.objects.get(username=username)
                if not hasattr(user, 'empleado') or user.empleado.numero_documento != numero_documento:
                    raise forms.ValidationError("El usuario y el número de documento proporcionados no coinciden.")
            except User.DoesNotExist:
                raise forms.ValidationError("El usuario y el número de documento proporcionados no coinciden.")
        return cleaned_data


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = '__all__'
        widgets = {
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_comercial': forms.TextInput(attrs={'class': 'form-control'}),
            'nit': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'logo_url': forms.URLInput(attrs={'class': 'form-control'}),
            'regimen': forms.Select(attrs={'class': 'form-select'}),
            'tipo_impuesto': forms.Select(attrs={'class': 'form-select'}),
            'porcentaje_impuesto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class SucursalForm(forms.ModelForm):
    class Meta:
        model = Sucursal
        fields = ['nombre', 'direccion', 'telefono', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


