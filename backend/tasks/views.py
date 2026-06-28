from rest_framework import viewsets, mixins
from .models import Tarea, Comentario, Estado, TareaUsuario
from .serializers import (
    TareaReadSerializer, TareaWriteSerializer,
    ComentarioSerializer, EstadoSerializer, AsignacionTareaSerializer
)
from .filters import TareaFilter, ComentarioFilter
from .permissions import TareaPermiso, ComentarioPermiso

class TareaViewSet(viewsets.ModelViewSet):
    permission_classes = [TareaPermiso] 
    filterset_class = TareaFilter  # Filtros

    def get_queryset(self):
        # Solo ves tareas de tus proyectos
        return Tarea.objects.filter(
            proyecto__equipo__usuario=self.request.user
        ).select_related('proyecto', 'estado').prefetch_related('responsables__usuario').distinct()

    # Django llama a este método antes de cada request para elegir el serializer correcto
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TareaReadSerializer   # GET → datos ricos
        return TareaWriteSerializer      # POST, PUT, PATCH → solo IDs

class AsignacionTareaViewSet(viewsets.ModelViewSet):
    queryset = TareaUsuario.objects.all()
    serializer_class = AsignacionTareaSerializer

class ComentarioViewSet(viewsets.ModelViewSet):
    permission_classes = [ComentarioPermiso] 
    filterset_class = ComentarioFilter  # Filtros
    serializer_class = ComentarioSerializer
    
    def get_queryset(self):
        return Comentario.objects.filter(
            tarea__proyecto__equipo__usuario=self.request.user
        ).select_related('usuario').distinct()
    
    def perform_create(self, serializer):
        # Tomamos el usuario del token, no del body
        serializer.save(usuario=self.request.user)

class EstadoViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer