import django_filters
from .models import Tarea, Comentario

class TareaFilter(django_filters.FilterSet):
    # Filtros exactos — buscan coincidencia exacta con el valor dado
    proyecto  = django_filters.NumberFilter(field_name='proyecto__id')
    estado    = django_filters.NumberFilter(field_name='estado__id')
    prioridad = django_filters.CharFilter(field_name='prioridad')

    # Filtro por responsable — busca tareas donde el usuario esté asignado
    responsable = django_filters.NumberFilter(field_name='responsables__usuario__id')

    # Filtros de rango de fechas — el frontend puede mandar una, la otra, o ambas
    fecha_limite_desde = django_filters.DateFilter(field_name='fecha_limite', lookup_expr='gte')
    fecha_limite_hasta = django_filters.DateFilter(field_name='fecha_limite', lookup_expr='lte')

    # Filtro de tareas vencidas — recibe true/false
    vencidas = django_filters.BooleanFilter(method='filtrar_vencidas')

    def filtrar_vencidas(self, queryset, name, value):
        from django.utils import timezone
        hoy = timezone.now().date()
        if value:  # si mandan ?vencidas=true
            return queryset.filter(
                fecha_limite__lt=hoy
            ).exclude(estado__nombre='Hecho')
        return queryset

    class Meta:
        model = Tarea
        fields = ['proyecto', 'estado', 'prioridad', 'responsable']


class ComentarioFilter(django_filters.FilterSet):
    tarea   = django_filters.NumberFilter(field_name='tarea__id')
    usuario = django_filters.NumberFilter(field_name='usuario__id')

    class Meta:
        model = Comentario
        fields = ['tarea', 'usuario']