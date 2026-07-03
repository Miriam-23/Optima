from rest_framework import serializers
from .models import Tarea, Comentario, TareaUsuario, Estado

# --- ESTADOS ---
class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = ['id', 'nombre']

# --- RESPONSABLES (solo lectura, anidado dentro de Tarea) ---
class TareaUsuarioReadSerializer(serializers.ModelSerializer):
    usuario_id = serializers.IntegerField(source='usuario.id', read_only=True)
    nombre = serializers.CharField(source='usuario.username', read_only=True)
    email = serializers.CharField(source='usuario.email', read_only=True)

    class Meta:
        model = TareaUsuario
        fields = ['usuario_id', 'nombre', 'email', 'fecha_asignacion']

# --- TAREA LECTURA (GET) ---
# Devuelve todo enriquecido para que el frontend pueda pintar sin peticiones extra
class TareaReadSerializer(serializers.ModelSerializer):
    nombre_proyecto = serializers.CharField(source='proyecto.nombre', read_only=True)
    nombre_estado = serializers.CharField(source='estado.nombre', read_only=True)
    responsables = TareaUsuarioReadSerializer(many=True, read_only=True)

    class Meta:
        model = Tarea
        fields = [
            'id', 'titulo', 'descripcion', 'fecha_creacion', 'fecha_limite',
            'fecha_finalizacion_real', 'esfuerzo_estimado', 'prioridad',
            'proyecto', 'nombre_proyecto',   # ID para operar + nombre para mostrar
            'estado', 'nombre_estado',       # ID para operar + nombre para mostrar
            'responsables'
        ]

# --- TAREA ESCRITURA (POST / PUT / PATCH) ---
# Solo acepta IDs, limpio y directo
class TareaWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = [
            'id', 'titulo', 'descripcion', 'fecha_limite',
            'fecha_finalizacion_real', 'esfuerzo_estimado',
            'prioridad', 'proyecto', 'estado'
        ]

    def validate(self, data):
        from django.utils import timezone
        from projects.models import ProyectoUsuario

        request = self.context.get('request')
        proyecto = data.get('proyecto')
        hoy = timezone.now().date()

        # Validación 1: solo el Project Manager puede crear/editar tareas
        if proyecto and request:
            es_pm = ProyectoUsuario.objects.filter(
                usuario=request.user,
                proyecto=proyecto,
                rol__nombre='Project Manager'
            ).exists()
            if not es_pm:
                raise serializers.ValidationError(
                    'Solo el Project Manager puede crear tareas en este proyecto.'
                )

        # Recuperar valores de la instancia en caso de PATCH parcial
        fecha_limite = data.get('fecha_limite')
        fecha_fin_real = data.get('fecha_finalizacion_real')

        if self.instance:
            fecha_limite = fecha_limite or self.instance.fecha_limite
            fecha_fin_real = fecha_fin_real or self.instance.fecha_finalizacion_real
        
        # Validación 2: la fecha límite no puede ser en el pasado (crear ni editar)
        if fecha_limite and fecha_limite < hoy:
            raise serializers.ValidationError({
                'fecha_limite': 'La fecha límite no puede ser una fecha pasada.'
            })
        
        # Validación 3: la fecha de finalización real no puede ser anterior a la fecha límite
        # Sí puede ser posterior (significa que se entregó tarde)
        if fecha_fin_real and fecha_limite and fecha_fin_real < fecha_limite:
            raise serializers.ValidationError({
                'fecha_finalizacion_real': 'La tarea no puede finalizar antes de su fecha límite.'
            })

        return data

# --- ASIGNACIÓN DE USUARIO A TAREA (POST / DELETE) ---
class AsignacionTareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TareaUsuario
        fields = ['id', 'tarea', 'usuario', 'fecha_asignacion']
        read_only_fields = ['fecha_asignacion']
    
    def validate(self, data):
        tarea = data.get('tarea')
        usuario = data.get('usuario')

        # Validación 1: el usuario debe pertenecer al proyecto de la tarea
        from projects.models import ProyectoUsuario
        pertenece = ProyectoUsuario.objects.filter(
            usuario=usuario,
            proyecto=tarea.proyecto
        ).exists()

        if not pertenece:
            raise serializers.ValidationError(
                'El usuario no pertenece al proyecto de esta tarea.'
            )

        # Validación 2: no asignar dos veces — unique_together ya lo protege,
        # pero el mensaje de Django es genérico
        if TareaUsuario.objects.filter(tarea=tarea, usuario=usuario).exists():
            raise serializers.ValidationError(
                'Este usuario ya está asignado a esta tarea.'
            )

        return data
    
# --- COMENTARIOS ---
class ComentarioSerializer(serializers.ModelSerializer):
    nombre_autor = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = Comentario
        fields = ['id', 'contenido', 'fecha_creacion', 'nombre_autor', 'usuario', 'tarea']
        read_only_fields = ['fecha_creacion', 'usuario'] # usuario ya no se acepta del body