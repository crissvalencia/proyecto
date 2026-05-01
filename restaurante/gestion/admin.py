from django.contrib import admin
from .models import (
    Empleado, Cliente, Mesa, Producto, Reserva,
    Orden, DetalleOrden, Factura, Insumo, Receta,
    Empresa, Sucursal,                              # NUEVO
)


class DetalleOrdenInline(admin.TabularInline):
    model = DetalleOrden
    extra = 1


class RecetaInline(admin.TabularInline):
    model = Receta
    extra = 1


# ── NUEVO: Sucursal dentro de Empresa ────────────────────────────────────────
class SucursalInline(admin.TabularInline):
    model  = Sucursal
    extra  = 1
    fields = ['nombre', 'direccion', 'telefono', 'activo']


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display  = ['razon_social', 'nit', 'regimen', 'tipo_impuesto', 'porcentaje_impuesto', 'activo']
    list_filter   = ['regimen', 'tipo_impuesto', 'activo']
    search_fields = ['razon_social', 'nit']
    inlines       = [SucursalInline]


@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display  = ['nombre', 'empresa', 'direccion', 'telefono', 'activo']
    list_filter   = ['activo', 'empresa']
    search_fields = ['nombre', 'empresa__razon_social']
# ─────────────────────────────────────────────────────────────────────────────


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display  = ['nombre', 'puesto', 'telefono', 'salario', 'activo']
    list_filter   = ['puesto', 'activo']
    search_fields = ['nombre']


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display  = ['nombre', 'telefono', 'email']
    search_fields = ['nombre']


@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ['numero', 'capacidad', 'disponible']
    list_filter  = ['disponible']


@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display  = ['nombre', 'cantidad', 'unidad_medida', 'stock_minimo']
    search_fields = ['nombre']


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display  = ['nombre', 'precio', 'fecha_actualizacion']
    search_fields = ['nombre']
    inlines       = [RecetaInline]


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'mesa', 'fecha', 'hora', 'estado']
    list_filter  = ['estado', 'fecha']


@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ['id', 'mesa', 'cliente', 'mesero', 'estado', 'total', 'fecha']
    list_filter  = ['estado']
    inlines      = [DetalleOrdenInline]


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display  = ['numero_factura', 'cliente', 'total', 'metodo_pago', 'fecha']
    search_fields = ['numero_factura']
    list_filter   = ['metodo_pago']


from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class EmpleadoInline(admin.StackedInline):
    model              = Empleado
    can_delete         = False
    verbose_name_plural = 'Perfil de Empleado'


class UserAdmin(BaseUserAdmin):
    inlines = (EmpleadoInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
