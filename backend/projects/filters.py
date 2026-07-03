import django_filters
from .models import ProyectoUsuario

class ProyectoUsuarioFilter(django_filters.FilterSet):
    proyecto = django_filters.NumberFilter(field_name='proyecto__id')
    usuario  = django_filters.NumberFilter(field_name='usuario__id')
    rol      = django_filters.NumberFilter(field_name='rol__id')

    class Meta:
        model = ProyectoUsuario
        fields = ['proyecto', 'usuario', 'rol']