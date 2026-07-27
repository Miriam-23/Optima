from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count
from .models import Proyecto, ProyectoUsuario
from .serializers import (
    ProyectoReadSerializer, ProyectoWriteSerializer,
    ProyectoUsuarioReadSerializer, ProyectoUsuarioWriteSerializer
)
from .filters import ProyectoUsuarioFilter
from .permissions import ProyectoPermiso, ProyectoUsuarioPermiso
from users.models import Rol
from notifications.utils import notificar_miembro, notificar_project_managers
from .services import DashboardService

class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all()
    permission_classes = [ProyectoPermiso]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ProyectoReadSerializer
        return ProyectoWriteSerializer
    
    def get_queryset(self):
        # Cada usuario solo ve los proyectos donde está asignado
        return Proyecto.objects.filter(
            equipo__usuario=self.request.user
        ).distinct()
    
    def perform_create(self, serializer):
        proyecto = serializer.save()
        try:
            rol_pm = Rol.objects.get(nombre='Project Manager')
            ProyectoUsuario.objects.create(
                usuario=self.request.user,
                proyecto=proyecto,
                rol=rol_pm
            )
        except Rol.DoesNotExist:
            # Si el rol no existe en la BD, el proyecto se crea igual
            # pero sin la asignación automática
            pass

    @action(detail=True, methods=['get'], url_path='dashboard')
    def dashboard(self, request, pk=None):
        proyecto = self.get_object()
        metricas = DashboardService.obtener_metricas_proyecto(proyecto)
        return Response(metricas)


class ProyectoUsuarioViewSet(viewsets.ModelViewSet):
    queryset = ProyectoUsuario.objects.select_related('usuario', 'proyecto', 'rol')
    permission_classes = [ProyectoUsuarioPermiso]
    filterset_class = ProyectoUsuarioFilter

    def perform_create(self, serializer):
        asignacion = serializer.save()
        # Notificar al nuevo miembro
        notificar_miembro(
            usuario=asignacion.usuario,
            tipo='miembro_agregado',
            mensaje=f'Fuiste agregado al proyecto "{asignacion.proyecto.nombre}" como {asignacion.rol.nombre}.'
        )
        # Notificar al PM
        notificar_project_managers(
            proyecto=asignacion.proyecto,
            tipo='miembro_agregado',
            mensaje=f'{asignacion.usuario.username} fue agregado al proyecto "{asignacion.proyecto.nombre}".'
        )

    def get_queryset(self):
        # Solo ves el equipo de tus proyectos
        return ProyectoUsuario.objects.filter(
            proyecto__equipo__usuario=self.request.user
        ).distinct()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ProyectoUsuarioReadSerializer
        return ProyectoUsuarioWriteSerializer