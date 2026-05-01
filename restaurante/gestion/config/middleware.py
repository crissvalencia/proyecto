from django.shortcuts import redirect
from django.urls import resolve
from django.conf import settings

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            # We don't want to redirect if they are already going to login or admin
            if not request.path.startswith('/admin/'):
                try:
                    current_route_name = resolve(request.path_info).url_name
                    if current_route_name not in ['login', 'logout', 'recuperar_clave']:
                        return redirect(settings.LOGIN_URL)
                except:
                    pass
        return self.get_response(request)
