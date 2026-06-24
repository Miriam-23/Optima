from rest_framework import serializers
from .models import Proyecto, ProyectoUsuario

class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = '__all__'  # Esto le dice a Django que traduzca todas las columnas a JSON

class ProyectoUsuarioSerializer(serializers.ModelSerializer):
    # Traemos la info masticada de las 3 llaves foráneas
    nombre_usuario = serializers.CharField(source='usuario.username', read_only=True)
    email_usuario = serializers.CharField(source='usuario.email', read_only=True)
    nombre_rol = serializers.CharField(source='rol.nombre', read_only=True)
    nombre_proyecto = serializers.CharField(source='proyecto.nombre', read_only=True)

    class Meta:
        model = ProyectoUsuario
        fields = '__all__'