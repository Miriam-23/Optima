from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count
from .models import Proyecto, ProyectoUsuario
from .serializers import (
    ProyectoReadSerializer, ProyectoWriteSerializer,
    ProyectoUsuarioReadSerializer, ProyectoUsuarioWriteSerializer
)
from .filters import ProyectoUsuarioFilter
from .permissions import ProyectoPermiso, ProyectoUsuarioPermiso
from users.models import Rol
from notifications.utils import notificar_miembro, notificar_project_managers

class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all()
    permission_classes = [ProyectoPermiso]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ProyectoReadSerializer
        return ProyectoWriteSerializer
    
    def get_queryset(self):
        # Cada usuario solo ve los proyectos donde está asignado
        return Proyecto.objects.filter(
            equipo__usuario=self.request.user
        ).distinct()
    
    def perform_create(self, serializer):
        proyecto = serializer.save()
        try:
            rol_pm = Rol.objects.get(nombre='Project Manager')
            ProyectoUsuario.objects.create(
                usuario=self.request.user,
                proyecto=proyecto,
                rol=rol_pm
            )
        except Rol.DoesNotExist:
            # Si el rol no existe en la BD, el proyecto se crea igual
            # pero sin la asignación automática
            pass

    @action(detail=True, methods=['get'], url_path='dashboard')
    def dashboard(self, request, pk=None):
        proyecto = self.get_object()
        hoy = timezone.now().date()

        tareas = proyecto.tareas.select_related('estado').prefetch_related('responsables__usuario')

        # --- 1. AVANCE GENERAL DEL PROYECTO ---
        total_tareas = tareas.count()
        tareas_completadas = tareas.filter(estado__nombre='Completado').count()
        avance_porcentaje = round((tareas_completadas / total_tareas) * 100) if total_tareas > 0 else 0

        # --- 2. TAREAS PENDIENTES ---
        tareas_pendientes = tareas.exclude(estado__nombre='Completado').count()

        # --- 3. TAREAS VENCIDAS ---
        tareas_vencidas = tareas.filter(
            fecha_limite__lt=hoy
        ).exclude(estado__nombre='Completado').count()

        # --- 4. RIESGO DE RETRASO ---
        en_3_dias = hoy + timezone.timedelta(days=3)
        tareas_en_riesgo = tareas.filter(
            fecha_limite__gte=hoy,
            fecha_limite__lte=en_3_dias
        ).exclude(estado__nombre='Completado').count()

        # --- 5. DISTRIBUCIÓN DE TAREAS POR ESTADO ---
        distribucion_estados = list(
            tareas.values('estado__nombre')
            .annotate(total=Count('id'))
            .order_by('estado__nombre')
        )

        # --- 6. CARGA DE TRABAJO Y DISTRIBUCIÓN POR INTEGRANTE ---
        miembros = proyecto.equipo.select_related('usuario', 'rol')
        carga_por_miembro = []

        for miembro in miembros:
            tareas_del_miembro = tareas.filter(responsables__usuario=miembro.usuario)
            total_miembro = tareas_del_miembro.count()
            completadas_miembro = tareas_del_miembro.filter(estado__nombre='Completado').count()
            vencidas_miembro = tareas_del_miembro.filter(
                fecha_limite__lt=hoy
            ).exclude(estado__nombre='Completado').count()
            esfuerzo_total = sum(
                t.esfuerzo_estimado for t in tareas_del_miembro if t.esfuerzo_estimado
            )

            carga_por_miembro.append({
                'id_asignacion': miembro.id,  # SOLUCIÓN AL 404: El ID real de la relación
                'usuario_id': miembro.usuario.id,
                'nombre': miembro.usuario.username,
                'email': miembro.usuario.email,
                'rol': miembro.rol.nombre,
                'total_tareas': total_miembro,
                'tareas_completadas': completadas_miembro,
                'tareas_vencidas': vencidas_miembro,
                'esfuerzo_estimado_total': esfuerzo_total,
            })
            
        # --- 7. ÚLTIMAS TAREAS (Para poblar la lista del frontend) ---
        # Ordenamos por fecha de creación descendente y tomamos las últimas 5
        ultimas_tareas_queryset = tareas.order_by('-fecha_creacion')[:5] 
        ultimas_tareas = [
            {
                'id': t.id,
                'titulo': t.titulo,
                'descripcion': getattr(t, 'descripcion', ''), # Por si no tienen descripción
                'estado': t.estado.nombre if t.estado else 'Sin estado'
            } for t in ultimas_tareas_queryset
        ]

        return Response({
            'proyecto_id': proyecto.id,
            'nombre': proyecto.nombre,
            'estado_general': proyecto.estado_general,
            'fecha_inicio': proyecto.fecha_inicio,
            'fecha_fin': proyecto.fecha_fin,

            'avance': {
                'total_tareas': total_tareas,
                'completadas': tareas_completadas,
                'porcentaje': avance_porcentaje,
            },

            'alertas': {
                'tareas_pendientes': tareas_pendientes,
                'tareas_vencidas': tareas_vencidas,
                'tareas_en_riesgo_retraso': tareas_en_riesgo,
            },

            'distribucion_por_estado': distribucion_estados,
            'carga_por_miembro': carga_por_miembro,
            
            'tareas': ultimas_tareas, # 🚀 NUEVO: Entregamos las tareas al frontend
        })

class ProyectoUsuarioViewSet(viewsets.ModelViewSet):
    queryset = ProyectoUsuario.objects.select_related('usuario', 'proyecto', 'rol')
    permission_classes = [ProyectoUsuarioPermiso]
    filterset_class = ProyectoUsuarioFilter

    def perform_create(self, serializer):
        asignacion = serializer.save()
        # Notificar al nuevo miembro
        notificar_miembro(
            usuario=asignacion.usuario,
            tipo='miembro_agregado',
            mensaje=f'Fuiste agregado al proyecto "{asignacion.proyecto.nombre}" como {asignacion.rol.nombre}.'
        )
        # Notificar al PM
        notificar_project_managers(
            proyecto=asignacion.proyecto,
            tipo='miembro_agregado',
            mensaje=f'{asignacion.usuario.username} fue agregado al proyecto "{asignacion.proyecto.nombre}".'
        )

    def get_queryset(self):
        # Solo ves el equipo de tus proyectos
        return ProyectoUsuario.objects.filter(
            proyecto__equipo__usuario=self.request.user
        ).distinct()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ProyectoUsuarioReadSerializer
        return ProyectoUsuarioWriteSerializer