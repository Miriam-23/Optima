from rest_framework import viewsets
from .models import Proyecto, ProyectoUsuario
from .serializers import ProyectoSerializer, ProyectoUsuarioSerializer

# Un ModelViewSet es una herramienta de Django REST Framework que en automático
# genera todas las operaciones básicas: Listar (GET), Crear (POST), Actualizar (PUT) y Borrar (DELETE).
class ProyectoViewSet(viewsets.ModelViewSet):
    # 1. Le decimos a Django de qué tabla tiene que sacar los datos
    queryset = Proyecto.objects.all()
    
    # 2. Le decimos qué traductor (Serializer) debe usar para empaquetar la información
    serializer_class = ProyectoSerializer

class ProyectoUsuarioViewSet(viewsets.ModelViewSet):
    queryset = ProyectoUsuario.objects.all()
    serializer_class = ProyectoUsuarioSerializer