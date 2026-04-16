from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def is_administrador(user):
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return hasattr(user, 'empleado') and user.empleado.puesto == 'administrador'

def admin_required(function=None, redirect_field_name=None, login_url=None):
    """
    Decorator for views that checks that the user is logged in
    and has the 'administrador' role.
    """
    actual_decorator = user_passes_test(
        is_administrador,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
