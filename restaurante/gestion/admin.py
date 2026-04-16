from django.contrib import admin
from .models import Empleado, Cliente, Mesa, Producto, Reserva, Orden, DetalleOrden, Factura, Insumo, Receta

class DetalleOrdenInline(admin.TabularInline):
    model = DetalleOrden
    extra = 1

class RecetaInline(admin.TabularInline):
    model = Receta
    extra = 1

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'puesto', 'telefono', 'salario', 'activo']
    list_filter = ['puesto', 'activo']
    search_fields = ['nombre']

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'telefono', 'email']
    search_fields = ['nombre']

@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ['numero', 'capacidad', 'disponible']
    list_filter = ['disponible']

@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'cantidad', 'unidad_medida', 'stock_minimo']
    search_fields = ['nombre']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'fecha_actualizacion']
    search_fields = ['nombre']
    inlines = [RecetaInline]

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'mesa', 'fecha', 'hora', 'estado']
    list_filter = ['estado', 'fecha']

@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ['id', 'mesa', 'cliente', 'mesero', 'estado', 'total', 'fecha']
    list_filter = ['estado']
    inlines = [DetalleOrdenInline]

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ['numero_factura', 'cliente', 'total', 'fecha']
    search_fields = ['numero_factura']

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# 1. Le decimos a Django que el Empleado va a ir "incrustado" dentro del Usuario
class EmpleadoInline(admin.StackedInline):
    model = Empleado
    can_delete = False
    verbose_name_plural = 'Perfil de Empleado'

# 2. Creamos un nuevo administrador de Usuarios que incluya al Empleado
class UserAdmin(BaseUserAdmin):
    inlines = (EmpleadoInline,)

# 3. Des-registramos el Usuario original y registramos el nuestro mejorado
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
