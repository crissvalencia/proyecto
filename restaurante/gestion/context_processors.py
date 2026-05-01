# gestion/context_processors.py
from django.db.models import F
from gestion.models import Insumo

def stock_alerts(request):
    """
    RF0013 — Inyecta el conteo de insumos bajo stock en todos los templates.
    """
    if not request.user.is_authenticated:
        return {}
    count = Insumo.objects.filter(cantidad__lte=F('stock_minimo')).count()
    return {'insumos_bajo_stock_count': count}
