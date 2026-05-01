from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied


def is_administrador(user):
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return hasattr(user, 'empleado') and user.empleado.puesto == 'administrador'


def admin_required(function=None, redirect_field_name=None, login_url='/login/'):
    actual_decorator = user_passes_test(
        is_administrador,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def is_cajero_or_admin(user):
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    if not hasattr(user, 'empleado'):
        return False
    return user.empleado.puesto in ('cajero', 'administrador')


def cajero_or_admin_required(function=None, redirect_field_name=None, login_url='/login/'):
    actual_decorator = user_passes_test(
        is_cajero_or_admin,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


# NUEVO — mesero puede gestionar órdenes, admin también
def is_mesero_or_admin(user):
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    if not hasattr(user, 'empleado'):
        return False
    return user.empleado.puesto in ('mesero', 'administrador')


def mesero_or_admin_required(function=None, redirect_field_name=None, login_url='/login/'):
    actual_decorator = user_passes_test(
        is_mesero_or_admin,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
