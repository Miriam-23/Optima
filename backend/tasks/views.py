from rest_framework import viewsets, mixins
from .models import Tarea, Comentario, Estado, TareaUsuario
from .serializers import (
    TareaReadSerializer, TareaWriteSerializer,
    ComentarioSerializer, EstadoSerializer, AsignacionTareaSerializer
)
from .filters import TareaFilter, ComentarioFilter
from .permissions import TareaPermiso, ComentarioPermiso
from notifications.utils import notificar_miembro, notificar_project_managers

class TareaViewSet(viewsets.ModelViewSet):
    permission_classes = [TareaPermiso]
    filterset_class = TareaFilter

    def get_queryset(self):
        return Tarea.objects.filter(
            proyecto__equipo__usuario=self.request.user
        ).select_related('proyecto', 'estado').prefetch_related('responsables__usuario').distinct()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TareaReadSerializer
        return TareaWriteSerializer

    def perform_create(self, serializer):
        tarea = serializer.save()
        notificar_project_managers(
            proyecto=tarea.proyecto,
            tipo='tarea_asignada',
            mensaje=f'Se creó la tarea "{tarea.titulo}" en el proyecto {tarea.proyecto.nombre}.'
        )

class AsignacionTareaViewSet(viewsets.ModelViewSet):
    queryset = TareaUsuario.objects.all()
    serializer_class = AsignacionTareaSerializer

    def perform_create(self, serializer):
        asignacion = serializer.save()
        notificar_miembro(
            usuario=asignacion.usuario,
            tipo='tarea_asignada',
            mensaje=f'Se te asignó la tarea "{asignacion.tarea.titulo}".'
        )
        notificar_project_managers(
            proyecto=asignacion.tarea.proyecto,
            tipo='tarea_asignada',
            mensaje=f'{asignacion.usuario.username} fue asignado a "{asignacion.tarea.titulo}".'
        )

class ComentarioViewSet(viewsets.ModelViewSet):
    permission_classes = [ComentarioPermiso]
    filterset_class = ComentarioFilter
    serializer_class = ComentarioSerializer

    def get_queryset(self):
        return Comentario.objects.filter(
            tarea__proyecto__equipo__usuario=self.request.user
        ).select_related('usuario').distinct()

    def perform_create(self, serializer):
        comentario = serializer.save(usuario=self.request.user)
        notificar_project_managers(
            proyecto=comentario.tarea.proyecto,
            tipo='comentario_nuevo',
            mensaje=f'{self.request.user.username} comentó en "{comentario.tarea.titulo}".'
        )

class EstadoViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer