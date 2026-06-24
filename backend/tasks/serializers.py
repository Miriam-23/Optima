from rest_framework import serializers
from .models import Tarea, Comentario, TareaUsuario, Estado

# TRADUCTOR 1: Serializador de la Tabla Intermedia (TareaUsuario)
class TareaUsuarioSerializer(serializers.ModelSerializer):
    # Viajamos a través del campo 'usuario' (FK) para extraer los datos reales de la BD
    usuario_id = serializers.IntegerField(source='usuario.id', read_only=True)
    nombre = serializers.CharField(source='usuario.username', read_only=True)
    email = serializers.CharField(source='usuario.email', read_only=True)

    class Meta:
        model = TareaUsuario
        # Exponemos los datos del usuario y la fecha en que se le asignó la tarea
        fields = ['usuario_id', 'nombre', 'email', 'fecha_asignacion']

class TareaSerializer(serializers.ModelSerializer):
    # Agregamos campos "virtuales" solo para lectura, extrayendo el nombre a través de la llave foránea
    nombre_proyecto = serializers.CharField(source='proyecto.nombre', read_only=True)
    nombre_estado = serializers.CharField(source='estado.nombre', read_only=True)
    
    # Django REST Framework busca automáticamente el related_name='responsables' 
    # que definimos en el modelo TareaUsuario y usa el traductor de arriba.
    responsables = TareaUsuarioSerializer(many=True, read_only=True)

    class Meta:
        model = Tarea
        fields = '__all__'  # Esto le dice a Django que traduzca todas las columnas a JSON

class AsignacionTareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TareaUsuario
        fields = '__all__'
        
class ComentarioSerializer(serializers.ModelSerializer):
    # Extraemos el nombre del autor para que el frontend pueda pintar el chat
    nombre_autor = serializers.CharField(source='usuario.username', read_only=True)
    
    class Meta:
        model = Comentario
        fields = '__all__'

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = '__all__'