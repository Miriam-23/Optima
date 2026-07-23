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

# --- RESPONSABLES PARA TARJETA KANBAN ---
class ResponsableCardSerializer(serializers.ModelSerializer):
    usuario_id = serializers.IntegerField(source='usuario.id', read_only=True)
    nombre = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = TareaUsuario
        fields = ['usuario_id', 'nombre']

# --- TAREA LISTADO/KANBAN (GET list) ---
# Información resumida para pintar tarjetas
class TareaReadSerializer(serializers.ModelSerializer):
    nombre_estado = serializers.CharField(source='estado.nombre', read_only=True)
    responsables = ResponsableCardSerializer(many=True, read_only=True)
    total_comentarios = serializers.IntegerField()

    class Meta:
        model = Tarea
        fields = [
            'id',
            'titulo',
            'prioridad',
            'fecha_limite',
            'estado',
            'nombre_estado',
            'responsables',
            'total_comentarios'
        ]

    def get_total_comentarios(self, obj):
        return obj.comentarios.count()

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
        hoy = timezone.now().date()

        # Validación 1: Todos pueden crear/editar tareas del proyecto, pero solo si pertenecen a él
        proyecto = data.get(
            'proyecto',
            self.instance.proyecto if self.instance else None
        )

        pertenece = ProyectoUsuario.objects.filter(
            usuario=request.user,
            proyecto=proyecto
        ).exists()

        if not pertenece:
            raise serializers.ValidationError(
                "No perteneces a este proyecto."
            )

        # ==============================
        # Validación 2:
        # Fecha límite
        # ==============================

        # SOLO validar si viene en la petición
        if 'fecha_limite' in data:

            fecha_limite = data.get('fecha_limite')

            if fecha_limite and fecha_limite < hoy:
                print("FALLO FECHA LIMITE VAL 2")

                raise serializers.ValidationError({
                    'fecha_limite':
                    'La fecha límite no puede ser una fecha pasada.'
                })


        # ==============================
        # Validación 3:
        # Fecha finalización real
        # ==============================

        if 'fecha_finalizacion_real' in data:

            fecha_fin_real = data.get('fecha_finalizacion_real')

            fecha_limite = data.get(
                'fecha_limite',
                self.instance.fecha_limite if self.instance else None
            )

            if (
                fecha_fin_real
                and fecha_limite
                and fecha_fin_real < fecha_limite
            ):
                print("FALLO FECHA LIMITE VAL 3")

                raise serializers.ValidationError({
                    'fecha_finalizacion_real':
                    'La tarea no puede finalizar antes de su fecha límite.'
                })


        print("DATOS VALIDANDO:", data)

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
    
# --- TAREA DETALLE (GET retrieve) ---
# Incluye comentarios y más detalles para la vista de detalle
class TareaDetailSerializer(serializers.ModelSerializer):
    nombre_proyecto = serializers.CharField(source='proyecto.nombre', read_only=True)
    nombre_estado = serializers.CharField(source='estado.nombre', read_only=True)
    responsables = TareaUsuarioReadSerializer(many=True, read_only=True)
    comentarios = serializers.SerializerMethodField()

    class Meta:
        model = Tarea
        fields = [
            'id', 'titulo', 'descripcion', 'fecha_creacion', 'fecha_limite',
            'fecha_finalizacion_real', 'esfuerzo_estimado', 'prioridad',
            'proyecto', 'nombre_proyecto',
            'estado', 'nombre_estado',
            'responsables', 'comentarios'
        ]

    def get_comentarios(self, obj):
        comentarios = obj.comentarios.all().order_by('-fecha_creacion')
        return ComentarioSerializer(comentarios, many=True, read_only=True).data

# --- COMENTARIOS ---
class ComentarioSerializer(serializers.ModelSerializer):
    nombre_autor = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = Comentario
        fields = ['id', 'contenido', 'fecha_creacion', 'nombre_autor', 'usuario', 'tarea']
        read_only_fields = ['fecha_creacion', 'usuario'] # usuario ya no se acepta del body