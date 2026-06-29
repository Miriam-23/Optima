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

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # create_user cifra la contraseña automáticamente
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user