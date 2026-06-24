from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProyectoViewSet, ProyectoUsuarioViewSet

# El Router se encarga de inventar y mapear las URLs automáticamente.
# Vinculará cosas como /api/projects/ con el método GET o POST de tu vista.
router = DefaultRouter()
router.register(r'projects', ProyectoViewSet, basename='proyecto')
router.register(r'team', ProyectoUsuarioViewSet, basename='equipo')

urlpatterns = [
    # Incluimos todas las rutas que el router genere de forma automática
    path('', include(router.urls)),
]