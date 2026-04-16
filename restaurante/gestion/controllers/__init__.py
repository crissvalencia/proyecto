from .dashboard_controller import dashboard
from .empleado_controller import empleado_list, empleado_create, empleado_update, empleado_delete
from .cliente_controller import cliente_list, cliente_create, cliente_update, cliente_delete
from .mesa_controller import mesa_list, mesa_create, mesa_update, mesa_delete
from .producto_controller import producto_list, producto_create, producto_update, producto_delete, categoria_list, categoria_create, categoria_update, categoria_delete
from .reserva_controller import reserva_list, reserva_create, reserva_update, reserva_delete
from .orden_controller import orden_list, orden_create, orden_detail, orden_agregar_detalle, orden_cambiar_estado, orden_delete
from .factura_controller import factura_list, factura_detail, generar_factura_auto
from .insumo_controller import insumo_list, insumo_create, insumo_update, insumo_delete
from .reporte_controller import reporte_ventas
from .auth_controller import crear_usuario_view, usuario_list_view

__all__ = [
    'dashboard',
    'empleado_list', 'empleado_create', 'empleado_update', 'empleado_delete',
    'cliente_list', 'cliente_create', 'cliente_update', 'cliente_delete',
    'mesa_list', 'mesa_create', 'mesa_update', 'mesa_delete',
    'producto_list', 'producto_create', 'producto_update', 'producto_delete',
    'categoria_list', 'categoria_create', 'categoria_update', 'categoria_delete',
    'reserva_list', 'reserva_create', 'reserva_update', 'reserva_delete',
    'orden_list', 'orden_create', 'orden_detail', 'orden_agregar_detalle', 'orden_cambiar_estado', 'orden_delete',
    'factura_list', 'factura_detail', 'generar_factura_auto',
    'insumo_list', 'insumo_create', 'insumo_update', 'insumo_delete',
    'reporte_ventas', 'crear_usuario_view', 'usuario_list_view',
]
