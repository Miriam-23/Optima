from rest_framework import viewsets, mixins
from .models import Tarea, Comentario, Estado, TareaUsuario
from .serializers import (
    TareaReadSerializer, TareaDetailSerializer, TareaWriteSerializer,
    ComentarioSerializer, EstadoSerializer, AsignacionTareaSerializer
)
from .filters import TareaFilter, ComentarioFilter
from .permissions import TareaPermiso, ComentarioPermiso
from notifications.utils import notificar_miembro, notificar_project_managers
from django.db.models import Count

class TareaViewSet(viewsets.ModelViewSet):
    permission_classes = [TareaPermiso]
    filterset_class = TareaFilter
    
    def get_queryset(self):
        queryset = Tarea.objects.filter(
            proyecto__equipo__usuario=self.request.user
        ).select_related(
            'proyecto',
            'estado'
        )

        if self.action == 'retrieve':
            queryset = queryset.prefetch_related(
                'responsables__usuario',
                'comentarios__usuario'
            )

        else:
            queryset = queryset.prefetch_related(
                'responsables__usuario'
            ).annotate(
                total_comentarios=Count('comentarios')
            )

        return queryset.distinct()

    def get_serializer_class(self):
            if self.action == 'retrieve':
                return TareaDetailSerializer
            if self.action == 'list':
                return TareaReadSerializer
            return TareaWriteSerializer

    def perform_create(self, serializer):
        tarea = serializer.save()
        notificar_project_managers(
            proyecto=tarea.proyecto,
            tipo='tarea_asignada',
            mensaje=f'Se creó la tarea "{tarea.titulo}" en el proyecto {tarea.proyecto.nombre}.'
        )
    
    def perform_update(self, serializer):
        tarea = serializer.save()

        responsable = self.request.data.get('responsable')

        if responsable:

            TareaUsuario.objects.filter(
                tarea=tarea
            ).delete()

            TareaUsuario.objects.create(
                tarea=tarea,
                usuario_id=responsable
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
        tarea = comentario.tarea
        proyecto = tarea.proyecto
        mensaje = f'{self.request.user.username} comentó en "{tarea.titulo}".'
        
        # Notificar a los responsables de la tarea
        for responsable in tarea.responsables.select_related('usuario'):
            if responsable.usuario != self.request.user:  # No te notificas a ti mismo
                notificar_miembro(
                    usuario=responsable.usuario,
                    tipo='comentario_nuevo',
                    mensaje=mensaje
                )

        # Notificar al PM si no es quien comentó
        notificar_project_managers(
            proyecto=proyecto,
            tipo='comentario_nuevo',
            mensaje=mensaje,
            excluir_usuario=self.request.user
        )

class EstadoViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer