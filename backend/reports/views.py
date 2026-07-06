from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from projects.models import Proyecto, ProyectoUsuario
from tasks.models import Tarea, TareaUsuario

class ReporteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuario = request.user
        hoy = timezone.now().date()

        # Detectar si el usuario es PM en algún proyecto
        es_pm = ProyectoUsuario.objects.filter(
            usuario=usuario,
            rol__nombre='Project Manager'
        ).exists()

        if es_pm:
            return self._reporte_pm(usuario, hoy)
        else:
            return self._reporte_miembro(usuario, hoy)

    def _reporte_miembro(self, usuario, hoy):
        # Proyectos donde participa
        proyectos = Proyecto.objects.filter(equipo__usuario=usuario).distinct()

        # Sus tareas
        mis_tareas = Tarea.objects.filter(
            responsables__usuario=usuario
        ).select_related('estado', 'proyecto')

        total_tareas = mis_tareas.count()
        completadas = mis_tareas.filter(estado__nombre='Hecho').count()
        en_progreso = mis_tareas.filter(estado__nombre='En progreso').count()
        pendientes = mis_tareas.exclude(
            estado__nombre__in=['Hecho', 'En progreso']
        ).count()
        vencidas = mis_tareas.filter(
            fecha_limite__lt=hoy
        ).exclude(estado__nombre='Hecho')

        # Carga por proyecto
        carga_por_proyecto = []
        for proyecto in proyectos:
            tareas_proyecto = mis_tareas.filter(proyecto=proyecto)
            carga_por_proyecto.append({
                'proyecto': proyecto.nombre,
                'total': tareas_proyecto.count(),
                'completadas': tareas_proyecto.filter(estado__nombre='Hecho').count(),
            })

        # Tareas críticas — vencidas o de alta prioridad sin completar
        tareas_criticas = list(
            mis_tareas.exclude(estado__nombre='Hecho')
            .filter(prioridad='Alta')
            .order_by('fecha_limite')
            .values('id', 'titulo', 'fecha_limite', 'prioridad', 'proyecto__nombre')[:5]
        )

        return Response({
            'rol': 'miembro',
            'tarjetas': {
                'proyectos_activos': proyectos.count(),
                'total_tareas': total_tareas,
                'completadas': completadas,
                'en_progreso': en_progreso,
                'pendientes': pendientes,
            },
            'grafica_dona': {
                'completadas': completadas,
                'en_progreso': en_progreso,
                'pendientes': pendientes,
                'vencidas': vencidas.count(),
            },
            'grafica_barras': carga_por_proyecto,
            'tareas_criticas': tareas_criticas,
        })

    def _reporte_pm(self, usuario, hoy):
        # Proyectos donde es PM
        proyectos = Proyecto.objects.filter(
            equipo__usuario=usuario,
            equipo__rol__nombre='Project Manager'
        ).distinct()

        # Todas las tareas de sus proyectos
        todas_tareas = Tarea.objects.filter(
            proyecto__in=proyectos
        ).select_related('estado', 'proyecto')

        total_tareas = todas_tareas.count()
        completadas = todas_tareas.filter(estado__nombre='Hecho').count()
        en_progreso = todas_tareas.filter(estado__nombre='En progreso').count()
        pendientes = todas_tareas.exclude(
            estado__nombre__in=['Hecho', 'En progreso']
        ).count()
        vencidas = todas_tareas.filter(
            fecha_limite__lt=hoy
        ).exclude(estado__nombre='Hecho').count()

        # Avance comparativo por proyecto para gráfica de barras
        avance_proyectos = []
        for proyecto in proyectos:
            tareas_p = todas_tareas.filter(proyecto=proyecto)
            total_p = tareas_p.count()
            completadas_p = tareas_p.filter(estado__nombre='Hecho').count()
            avance_proyectos.append({
                'proyecto': proyecto.nombre,
                'total': total_p,
                'completadas': completadas_p,
                'porcentaje': round((completadas_p / total_p) * 100) if total_p > 0 else 0,
            })

        # Fuegos por apagar — tareas vencidas o de alta prioridad
        fuegos = list(
            todas_tareas.exclude(estado__nombre='Hecho')
            .filter(prioridad='Alta')
            .order_by('fecha_limite')
            .values('id', 'titulo', 'fecha_limite', 'prioridad', 'proyecto__nombre')[:5]
        )

        return Response({
            'rol': 'project_manager',
            'tarjetas': {
                'proyectos_activos': proyectos.count(),
                'total_tareas': total_tareas,
                'completadas': completadas,
                'en_progreso': en_progreso,
                'pendientes': pendientes,
            },
            'grafica_dona': {
                'completadas': completadas,
                'en_progreso': en_progreso,
                'pendientes': pendientes,
                'vencidas': vencidas,
            },
            'grafica_barras': avance_proyectos,
            'tareas_criticas': fuegos,
        })