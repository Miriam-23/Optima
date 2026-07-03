from .models import Notificacion
from projects.models import ProyectoUsuario
from .emails import enviar_correo_notificacion

def notificar_miembro(usuario, tipo, mensaje):
    Notificacion.objects.create(usuario=usuario, tipo=tipo, mensaje=mensaje)
    enviar_correo_notificacion(usuario, tipo, mensaje)  

def notificar_project_managers(proyecto, tipo, mensaje, excluir_usuario=None):
    pms = ProyectoUsuario.objects.filter(
        proyecto=proyecto,
        rol__nombre='Project Manager'
    ).select_related('usuario')
    for pm in pms:
        if excluir_usuario and pm.usuario == excluir_usuario:
            continue  # No te notificas a ti mismo
        notificar_miembro(pm.usuario, tipo, mensaje)

def notificar_equipo_completo(proyecto, tipo, mensaje):
    miembros = ProyectoUsuario.objects.filter(
        proyecto=proyecto
    ).select_related('usuario')
    for miembro in miembros:
        notificar_miembro(miembro.usuario, tipo, mensaje)