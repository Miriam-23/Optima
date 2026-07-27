from projects.models import Proyecto
from tasks.models import TareaUsuario
from django.utils import timezone
from projects.models import ProyectoUsuario
from projects.models import Proyecto
from projects.services import DashboardService

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
            tarea.estado.nombre != 'Completada'
        )
        estado_label = f'{tarea.estado.nombre} (VENCIDA)' if vencida else tarea.estado.nombre
        lineas.append(
            f'- [{tarea.proyecto.nombre}] {tarea.titulo} | '
            f'Estado: {estado_label} | '
            f'Prioridad: {tarea.prioridad} | '
            f'Vence: {tarea.fecha_limite}'
        )

    return '\n'.join(lineas)


def obtener_contexto_equipo(usuario) -> str:
    """
    Obtiene los miembros del equipo en los proyectos donde participa el usuario.
    """

    proyectos_usuario = ProyectoUsuario.objects.filter(
        usuario=usuario
    ).values_list('proyecto_id', flat=True).distinct()

    if not proyectos_usuario:
        return 'EQUIPO DE TRABAJO:\nEl usuario no pertenece a ningún proyecto.'

    asignaciones = ProyectoUsuario.objects.filter(
        proyecto_id__in=proyectos_usuario
    ).select_related(
        'usuario',
        'proyecto',
        'rol'
    ).order_by('proyecto__nombre')

    if not asignaciones.exists():
        return 'EQUIPO DE TRABAJO:\nNo hay miembros registrados en los proyectos.'

    lineas = ['EQUIPO DE TRABAJO:']
    proyecto_actual = None

    for asignacion in asignaciones:
        nombre_proyecto = asignacion.proyecto.nombre

        if nombre_proyecto != proyecto_actual:
            lineas.append(f'\nProyecto: {nombre_proyecto}')
            proyecto_actual = nombre_proyecto

        es_yo = ' (tú)' if asignacion.usuario == usuario else ''

        lineas.append(
            f'  - {asignacion.usuario.username}{es_yo} | '
            f'Rol: {asignacion.rol.nombre}'
        )

    return '\n'.join(lineas)

#  Contexto de métricas del dashboard del usuario
def obtener_contexto_dashboard(usuario) -> str:
    """
    Usa DashboardService para obtener métricas consistentes
    con las que ve el usuario en la app, sin duplicar lógica.
    """
    proyectos = Proyecto.objects.filter(
        equipo__usuario=usuario
    ).distinct()

    if not proyectos.exists():
        return 'MÉTRICAS DE PROYECTOS:\nNo hay proyectos disponibles.'

    lineas = ['MÉTRICAS DE PROYECTOS:']

    for proyecto in proyectos:
        m = DashboardService.obtener_metricas_proyecto(proyecto)

        dist_texto = ', '.join(
            f"{d['estado__nombre']}: {d['total']}"
            for d in m['distribucion_por_estado']
        )

        lineas.append(
            f'\nProyecto: {m["nombre"]} | Estado: {m["estado_general"]}'
        )
        lineas.append(
            f'  Avance: {m["avance"]["porcentaje"]}% '
            f'({m["avance"]["completadas"]}/{m["avance"]["total_tareas"]} completadas)'
        )
        lineas.append(
            f'  Vencidas: {m["alertas"]["tareas_vencidas"]} | '
            f'En riesgo: {m["alertas"]["tareas_en_riesgo_retraso"]}'
        )
        if dist_texto:
            lineas.append(f'  Distribución: {dist_texto}')

        for miembro in m['carga_por_miembro']:
            pendientes = (
                miembro["total_tareas"] -
                miembro["tareas_completadas"]
            )

            lineas.append(
                f'  - {miembro["nombre"]} ({miembro["rol"]}): '
                f'Total asignadas: {miembro["total_tareas"]}, '
                f'Completadas: {miembro["tareas_completadas"]}, '
                f'Pendientes: {pendientes}, '
                f'Vencidas: {miembro["tareas_vencidas"]}'
            )

    return '\n'.join(lineas)