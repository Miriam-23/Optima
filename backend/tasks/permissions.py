from rest_framework.permissions import BasePermission
from projects.models import ProyectoUsuario

def es_project_manager(usuario, proyecto):
    return ProyectoUsuario.objects.filter(
        usuario=usuario,
        proyecto=proyecto,
        rol__nombre='Project Manager'
    ).exists()

def es_miembro(usuario, proyecto):
    return ProyectoUsuario.objects.filter(
        usuario=usuario,
        proyecto=proyecto
    ).exists()

# ── PERMISO PARA TAREAS ───────────────────────
class TareaPermiso(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        usuario = request.user
        proyecto = obj.proyecto

        # Eliminar sigue siendo exclusivo del PM
        if view.action == 'destroy':
            return es_project_manager(usuario, proyecto)

        # Todo lo demás requiere pertenecer al proyecto
        return es_miembro(usuario, proyecto)

# ── PERMISO PARA COMENTARIOS ──────────────────
class ComentarioPermiso(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        usuario = request.user
        # Solo puedes eliminar tu propio comentario, o ser PM
        if view.action == 'destroy':
            return obj.usuario == usuario or es_project_manager(usuario, obj.tarea.proyecto)
        return es_miembro(usuario, obj.tarea.proyecto)