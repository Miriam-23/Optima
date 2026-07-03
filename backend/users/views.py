from rest_framework import viewsets, mixins, generics, status
from django.contrib.auth.models import User
from .models import Rol
from .serializers import UserSerializer, RolSerializer, RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import LoginSerializer

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_active=True) # Solo enviamos usuarios activos
    serializer_class = UserSerializer

class RolViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'mensaje': 'Sesión cerrada correctamente.'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'error': 'Token inválido o ya expirado.'}, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]  # Este endpoint NO requiere token
    serializer_class = RegisterSerializer

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

from .models import TokenVerificacion
from django.contrib.auth.models import User

class VerificarCorreoView(APIView):
    permission_classes = []  # No requiere token

    def get(self, request, token):
        try:
            token_obj = TokenVerificacion.objects.select_related('usuario').get(token=token)
        except TokenVerificacion.DoesNotExist:
            return Response(
                {'error': 'Enlace de verificación inválido.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if token_obj.ha_expirado():
            token_obj.delete()
            return Response(
                {'error': 'El enlace ha expirado. Regístrate nuevamente.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        usuario = token_obj.usuario
        usuario.is_active = True
        usuario.save()
        token_obj.delete()  # El token ya no sirve después de usarse

        return Response(
            {'mensaje': f'Cuenta de {usuario.username} verificada correctamente. Ya puedes iniciar sesión.'},
            status=status.HTTP_200_OK
        )