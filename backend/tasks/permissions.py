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
        # Ver y comentar: cualquier miembro
        if view.action in ['retrieve']:
            return es_miembro(usuario, proyecto)
        # Cambiar estado de su propia tarea: miembro asignado
        if view.action in ['partial_update']:
            es_responsable = obj.responsables.filter(usuario=usuario).exists()
            if es_responsable:
                return True
        # Crear, editar completo, eliminar: solo PM
        return es_project_manager(usuario, proyecto)

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