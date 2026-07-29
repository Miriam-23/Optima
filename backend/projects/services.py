from django.utils import timezone
from django.db.models import Count

class DashboardService:

    @staticmethod
    def obtener_metricas_proyecto(proyecto) -> dict:
        """
        Calcula todas las métricas de un proyecto.

        Este servicio es reutilizable y puede ser utilizado tanto por:
        - La API del dashboard (/api/projects/{id}/dashboard/)
        - El chatbot (para responder preguntas sobre métricas)

        De esta manera se evita duplicar lógica (Principio DRY).
        """

        hoy = timezone.now().date()
        en_3_dias = hoy + timezone.timedelta(days=3)

        tareas = proyecto.tareas.select_related('estado').prefetch_related(
            'responsables__usuario'
        )

        # --- 1. AVANCE GENERAL DEL PROYECTO ---
        total_tareas = tareas.count()
        tareas_completadas = tareas.filter(estado__nombre='Completada').count()
        avance_porcentaje = (
            round((tareas_completadas / total_tareas) * 100)
            if total_tareas > 0 else 0
        )

        # --- 2. TAREAS PENDIENTES ---
        tareas_pendientes = tareas.exclude(
            estado__nombre='Completada'
        ).count()

        # --- 3. TAREAS VENCIDAS ---
        tareas_vencidas = tareas.filter(
            fecha_limite__lt=hoy
        ).exclude(
            estado__nombre='Completada'
        ).count()

        # --- 4. TAREAS EN RIESGO DE RETRASO ---
        tareas_en_riesgo = tareas.filter(
            fecha_limite__gte=hoy,
            fecha_limite__lte=en_3_dias
        ).exclude(
            estado__nombre='Completada'
        ).count()

        # --- 5. DISTRIBUCIÓN DE TAREAS POR ESTADO ---
        distribucion_estados = list(
            tareas.values('estado__nombre')
            .annotate(total=Count('id'))
            .order_by('estado__nombre')
        )

        # --- 6. CARGA DE TRABAJO POR MIEMBRO ---
        miembros = proyecto.equipo.select_related('usuario', 'rol')
        carga_por_miembro = []

        for miembro in miembros:
            tareas_miembro = tareas.filter(
                responsables__usuario=miembro.usuario
            )

            total_miembro = tareas_miembro.count()
            completadas_miembro = tareas_miembro.filter(
                estado__nombre='Completada'
            ).count()

            vencidas_miembro = tareas_miembro.filter(
                fecha_limite__lt=hoy
            ).exclude(
                estado__nombre='Completada'
            ).count()

            esfuerzo_total = sum(
                t.esfuerzo_estimado
                for t in tareas_miembro
                if t.esfuerzo_estimado
            )

            carga_por_miembro.append({
                'usuario_id': miembro.usuario.id,
                'nombre': miembro.usuario.username,
                'email': miembro.usuario.email,
                'rol': miembro.rol.nombre,
                'total_tareas': total_miembro,
                'tareas_completadas': completadas_miembro,
                'tareas_vencidas': vencidas_miembro,
                'esfuerzo_estimado_total': esfuerzo_total,
            })

        # --- 7. ÚLTIMAS TAREAS DEL PROYECTO ---
        ultimas_tareas_queryset = tareas.order_by(
            '-fecha_creacion'
        )[:5]

        ultimas_tareas = [
            {
                'id': t.id,
                'titulo': t.titulo,
                'descripcion': getattr(t, 'descripcion', ''),
                'estado': t.estado.nombre if t.estado else 'Sin estado'
            }
            for t in ultimas_tareas_queryset
        ]

        # --- RESPUESTA FINAL DEL DASHBOARD ---
        return {

            # Información general del proyecto
            'proyecto_id': proyecto.id,
            'nombre': proyecto.nombre,
            'descripcion': proyecto.descripcion,
            'estado_general': proyecto.estado_general,
            'fecha_inicio': proyecto.fecha_inicio,
            'fecha_fin': proyecto.fecha_fin,

            # Métricas de avance
            'avance': {
                'total_tareas': total_tareas,
                'completadas': tareas_completadas,
                'porcentaje': avance_porcentaje,
            },

            # Alertas del proyecto
            'alertas': {
                'tareas_pendientes': tareas_pendientes,
                'tareas_vencidas': tareas_vencidas,
                'tareas_en_riesgo_retraso': tareas_en_riesgo,
            },

            # Distribución de tareas por estado
            'distribucion_por_estado': distribucion_estados,

            # Estadísticas de carga por integrante
            'carga_por_miembro': carga_por_miembro,

            # Últimas tareas creadas (para el frontend)
            'tareas': ultimas_tareas
        }