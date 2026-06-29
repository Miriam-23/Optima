from rest_framework.permissions import BasePermission
from .models import ProyectoUsuario

def es_project_manager(usuario, proyecto):
    """Verifica si el usuario es Project Manager en el proyecto dado."""
    return ProyectoUsuario.objects.filter(
        usuario=usuario,
        proyecto=proyecto,
        rol__nombre='Project Manager'
    ).exists()

def es_miembro(usuario, proyecto):
    """Verifica si el usuario pertenece al proyecto, con cualquier rol."""
    return ProyectoUsuario.objects.filter(
        usuario=usuario,
        proyecto=proyecto
    ).exists()

# ── PERMISO PARA PROYECTOS ────────────────────
class ProyectoPermiso(BasePermission):
    def has_permission(self, request, view):
        # Cualquier usuario autenticado puede ver la lista
        if view.action == 'list':
            return request.user.is_authenticated
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        usuario = request.user
        # Ver detalle: cualquier miembro del proyecto
        if view.action in ['retrieve', 'dashboard']:
            return es_miembro(usuario, obj)
        # Editar o eliminar: solo Project Manager
        return es_project_manager(usuario, obj)

# ── PERMISO PARA EQUIPO DEL PROYECTO ─────────
class ProyectoUsuarioPermiso(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated
        if view.action == 'create':
            # Para crear, verificamos en validate() del serializer
            # Aquí solo verificamos que esté autenticado
            return request.user.is_authenticated
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        usuario = request.user
        if view.action == 'retrieve':
            return es_miembro(usuario, obj.proyecto)
        # Solo el PM puede agregar o remover miembros
        return es_project_manager(usuario, obj.proyecto)