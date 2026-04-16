from django.urls import path
from .controllers import (
    dashboard,
    empleado_list, empleado_create, empleado_update, empleado_delete,
    cliente_list, cliente_create, cliente_update, cliente_delete,
    mesa_list, mesa_create, mesa_update, mesa_delete,
    producto_list, producto_create, producto_update, producto_delete,
    categoria_list, categoria_create, categoria_update, categoria_delete,
    reserva_list, reserva_create, reserva_update, reserva_delete,
    orden_list, orden_create, orden_detail, orden_agregar_detalle, orden_cambiar_estado, orden_delete,
    factura_list, factura_detail,
    insumo_list, insumo_create, insumo_update, insumo_delete,
    reporte_ventas,
    crear_usuario_view, usuario_list_view,
)
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(template_name='gestion/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', dashboard, name='dashboard'),
    # Empleados (RF001)
    path('empleados/', empleado_list, name='empleado_list'),
    path('empleados/crear/', empleado_create, name='empleado_create'),
    path('empleados/<int:pk>/editar/', empleado_update, name='empleado_update'),
    path('empleados/<int:pk>/eliminar/', empleado_delete, name='empleado_delete'),
    # Clientes
    path('clientes/', cliente_list, name='cliente_list'),
    path('clientes/crear/', cliente_create, name='cliente_create'),
    path('clientes/<int:pk>/editar/', cliente_update, name='cliente_update'),
    path('clientes/<int:pk>/eliminar/', cliente_delete, name='cliente_delete'),
    # Mesas
    path('mesas/', mesa_list, name='mesa_list'),
    path('mesas/crear/', mesa_create, name='mesa_create'),
    path('mesas/<int:pk>/editar/', mesa_update, name='mesa_update'),
    path('mesas/<int:pk>/eliminar/', mesa_delete, name='mesa_delete'),
    # Productos (RF007)
    path('productos/', producto_list, name='producto_list'),
    path('productos/crear/', producto_create, name='producto_create'),
    path('productos/<int:pk>/editar/', producto_update, name='producto_update'),
    path('productos/<int:pk>/eliminar/', producto_delete, name='producto_delete'),
    # Categorias (RF007)
    path('categorias/', categoria_list, name='categoria_list'),
    path('categorias/crear/', categoria_create, name='categoria_create'),
    path('categorias/<int:pk>/editar/', categoria_update, name='categoria_update'),
    path('categorias/<int:pk>/eliminar/', categoria_delete, name='categoria_delete'),
    # Reservas (RF004)
    path('reservas/', reserva_list, name='reserva_list'),
    path('reservas/crear/', reserva_create, name='reserva_create'),
    path('reservas/<int:pk>/editar/', reserva_update, name='reserva_update'),
    path('reservas/<int:pk>/eliminar/', reserva_delete, name='reserva_delete'),
    # Ordenes (RF008)
    path('ordenes/', orden_list, name='orden_list'),
    path('ordenes/crear/', orden_create, name='orden_create'),
    path('ordenes/<int:pk>/', orden_detail, name='orden_detail'),
    path('ordenes/<int:pk>/agregar-detalle/', orden_agregar_detalle, name='orden_agregar_detalle'),
    path('ordenes/<int:pk>/cambiar-estado/', orden_cambiar_estado, name='orden_cambiar_estado'),
    path('ordenes/<int:pk>/eliminar/', orden_delete, name='orden_delete'),
    # Facturas (RF005)
    path('facturas/', factura_list, name='factura_list'),
    path('facturas/<int:pk>/', factura_detail, name='factura_detail'),
    # Insumos
    path('insumos/', insumo_list, name='insumo_list'),
    path('insumos/crear/', insumo_create, name='insumo_create'),
    path('insumos/<int:pk>/editar/', insumo_update, name='insumo_update'),
    path('insumos/<int:pk>/eliminar/', insumo_delete, name='insumo_delete'),
    # Reportes (RF012)
    path('reportes/ventas/', reporte_ventas, name='reporte_ventas'),
    # Usuarios (Auth)
    path('usuarios/', usuario_list_view, name='usuario_list'),
    path('usuarios/crear/', crear_usuario_view, name='crear_usuario'),
]