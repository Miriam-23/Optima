from rest_framework import viewsets
from .models import Tarea, Comentario, Estado, TareaUsuario
from .serializers import TareaSerializer, ComentarioSerializer, EstadoSerializer, AsignacionTareaSerializer

class TareaViewSet(viewsets.ModelViewSet):
    # 1. Le decimos a Django de qué tabla tiene que sacar los datos
    queryset = Tarea.objects.all()
    
    # 2. Le decimos qué traductor (Serializer) debe usar para empaquetar la información
    serializer_class = TareaSerializer

class AsignacionTareaViewSet(viewsets.ModelViewSet):
    queryset = TareaUsuario.objects.all()
    serializer_class = AsignacionTareaSerializer

class ComentarioViewSet(viewsets.ModelViewSet):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer

class EstadoViewSet(viewsets.ModelViewSet):
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer