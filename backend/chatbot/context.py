from projects.models import Proyecto


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