from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TareaViewSet, ComentarioViewSet, EstadoViewSet, AsignacionTareaViewSet

router = DefaultRouter()
router.register(r'tasks', TareaViewSet, basename='tarea')
router.register(r'assignments', AsignacionTareaViewSet, basename='asignacion')
router.register(r'comments', ComentarioViewSet, basename='comentario')
router.register(r'statuses', EstadoViewSet, basename='estado')

urlpatterns = [
    # Incluimos todas las rutas que el router genere de forma automática
    path('', include(router.urls)),
]