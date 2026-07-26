from projects.models import Proyecto
from tasks.models import TareaUsuario
from django.utils import timezone

# Contexto de proyectos del usuario
def obtener_contexto_proyectos(usuario):

    proyectos = Proyecto.objects.filter(
        equipo__usuario=usuario
    ).distinct()


    if not proyectos.exists():
        return (
            "PROYECTOS DEL USUARIO:\n"
            "El usuario no tiene proyectos asignados actualmente."
        )


    lineas = [
        "PROYECTOS DEL USUARIO:"
    ]


    for proyecto in proyectos:

        lineas.append(
            f"""
- Nombre: {proyecto.nombre}
  Estado: {proyecto.estado_general}
  Inicio: {proyecto.fecha_inicio}
  Fin: {proyecto.fecha_fin if proyecto.fecha_fin else "No definido"}
"""
        )


    return "\n".join(lineas)

# Contexto de tareas asignadas al usuario
def obtener_contexto_tareas(usuario) -> str:
    """
    Obtiene las tareas asignadas al usuario autenticado
    y las formatea como texto para el system prompt.
    """

    hoy = timezone.now().date()

    asignaciones = TareaUsuario.objects.filter(
        usuario=usuario
    ).select_related('tarea', 'tarea__estado', 'tarea__proyecto')

    if not asignaciones.exists():
        return 'TAREAS ASIGNADAS AL USUARIO:\nEl usuario no tiene tareas asignadas actualmente.'

    lineas = ['TAREAS ASIGNADAS AL USUARIO:']

    for asignacion in asignaciones:
        tarea = asignacion.tarea
        vencida = (
            tarea.fecha_limite < hoy and
            tarea.estado.nombre != 'Hecho'
        )
        estado_label = f'{tarea.estado.nombre} (VENCIDA)' if vencida else tarea.estado.nombre
        lineas.append(
            f'- [{tarea.proyecto.nombre}] {tarea.titulo} | '
            f'Estado: {estado_label} | '
            f'Prioridad: {tarea.prioridad} | '
            f'Vence: {tarea.fecha_limite}'
        )

    return '\n'.join(lineas)