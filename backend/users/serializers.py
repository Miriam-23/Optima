from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Rol  # Importamos también Rol ya que vive en esta app

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Solo exponemos datos públicos e inofensivos
        fields = ['id', 'username', 'email', 'is_active', 'date_joined']

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'