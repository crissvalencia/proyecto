from django.shortcuts import render
from django.db.models import Sum, Count
from django.utils import timezone
from gestion.models import Orden, DetalleOrden

def reporte_ventas(request):
    hoy = timezone.now().date()
    anio = hoy.year

    if hoy.month <= 6:
        # Estamos en el primer semestre
        inicio_actual = hoy.replace(month=1, day=1)
        fin_actual = hoy.replace(month=6, day=30)
        inicio_anterior = hoy.replace(year=anio-1, month=7, day=1)
        fin_anterior = hoy.replace(year=anio-1, month=12, day=31)
        nombre_actual = f"Primer semestre {anio}"
        nombre_anterior = f"Segundo semestre {anio-1}"
    else:
        # Estamos en el segundo semestre
        inicio_actual = hoy.replace(month=7, day=1)
        fin_actual = hoy.replace(month=12, day=31)
        inicio_anterior = hoy.replace(month=1, day=1)
        fin_anterior = hoy.replace(month=6, day=30)
        nombre_actual = f"Segundo semestre {anio}"
        nombre_anterior = f"Primer semestre {anio}"

    def get_stats(inicio, fin):
        import datetime
        inicio_dt = timezone.make_aware(datetime.datetime.combine(inicio, datetime.time.min))
        fin_dt = timezone.make_aware(datetime.datetime.combine(fin, datetime.time.max))

        ordenes = Orden.objects.filter(
            fecha__gte=inicio_dt,
            fecha__lte=fin_dt,
            estado='entregada'
        )
        total_ventas = ordenes.aggregate(total=Sum('total'))['total'] or 0
        total_ordenes = ordenes.count()
        top_productos = DetalleOrden.objects.filter(
            orden__in=ordenes
        ).values(
            'producto__nombre'
        ).annotate(
            total_vendido=Sum('cantidad')
        ).order_by('-total_vendido')[:3]

        return {
            'total_ventas': total_ventas,
            'total_ordenes': total_ordenes,
            'top_productos': top_productos,
        }

    context = {
        'nombre_actual': nombre_actual,
        'nombre_anterior': nombre_anterior,
        'semestre_actual': get_stats(inicio_actual, fin_actual),
        'semestre_anterior': get_stats(inicio_anterior, fin_anterior),
    }
    return render(request, 'gestion/reporte_de_ventas.html', context)