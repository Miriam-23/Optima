from rest_framework import serializers
from .models import Proyecto, ProyectoUsuario

# --- PROYECTO LECTURA (GET) ---
class ProyectoReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = [
            'id', 'nombre', 'descripcion',
            'fecha_inicio', 'fecha_fin', 'estado_general'
        ]

# --- PROYECTO ESCRITURA (POST / PUT / PATCH) ---
class ProyectoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = [
            'nombre', 'descripcion',
            'fecha_inicio', 'fecha_fin', 'estado_general'
        ]
    
    def validate(self, data):
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')

        # En PATCH, los campos no enviados no llegan en data, 
        # así que los rescatamos de la instancia existente
        if self.instance:
            fecha_inicio = fecha_inicio or self.instance.fecha_inicio
            fecha_fin = fecha_fin or self.instance.fecha_fin

        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            raise serializers.ValidationError({
                'fecha_fin': 'La fecha de fin no puede ser anterior a la fecha de inicio.'
            })

        return data

# --- MIEMBRO DE PROYECTO LECTURA (GET) ---
class ProyectoUsuarioReadSerializer(serializers.ModelSerializer):
    nombre_usuario = serializers.CharField(source='usuario.username', read_only=True)
    email_usuario = serializers.CharField(source='usuario.email', read_only=True)
    nombre_rol = serializers.CharField(source='rol.nombre', read_only=True)
    nombre_proyecto = serializers.CharField(source='proyecto.nombre', read_only=True)

    class Meta:
        model = ProyectoUsuario
        fields = [
            'id',
            'usuario', 'nombre_usuario', 'email_usuario',  # ID + datos legibles
            'proyecto', 'nombre_proyecto',                  # ID + datos legibles
            'rol', 'nombre_rol',                            # ID + datos legibles
            'fecha_asignacion'
        ]

# --- MIEMBRO DE PROYECTO ESCRITURA (POST / PUT / PATCH) ---
class ProyectoUsuarioWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProyectoUsuario
        fields = ['usuario', 'proyecto', 'rol']
    
    def validate(self, data):
        # unique_together ya lo maneja el modelo, pero este mensaje es más claro para el frontend
        usuario = data.get('usuario')
        proyecto = data.get('proyecto')
        rol = data.get('rol')

        if ProyectoUsuario.objects.filter(usuario=usuario, proyecto=proyecto, rol=rol).exists():
            raise serializers.ValidationError(
                'Este usuario ya tiene ese rol asignado en el proyecto.'
            )
        return data