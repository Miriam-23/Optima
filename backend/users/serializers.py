from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Rol  # Importamos también Rol ya que vive en esta app
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import hashlib
from .models import TokenVerificacion
from notifications.emails import enviar_correo_verificacion

class UserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        # Solo exponemos datos públicos e inofensivos
        fields = ['id', 'username', 'email', 'is_active', 'date_joined', 'avatar_url']
    
    def get_avatar_url(self, obj):
        email = obj.email.lower().strip() if obj.email else ''
        hash_email = hashlib.md5(email.encode()).hexdigest()
        return f'https://www.gravatar.com/avatar/{hash_email}?d=identicon&s=200'

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
        'username': {'validators': []}  # Desactiva los validadores por defecto de Django
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Ya existe una cuenta registrada con este correo.'
            )
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'Este nombre de usuario ya está en uso.'
            )
        return value

    def create(self, validated_data):
        # Cuenta inactiva hasta verificar correo
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False  # ← no puede loguearse aún
        )
        # Crear token de verificación
        token = TokenVerificacion.objects.create(usuario=user)
        # Enviar correo
        enviar_correo_verificacion(user, token.token)
        return user
    
class LoginSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        return super().get_token(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        data["user"] = UserSerializer(self.user).data

        return data