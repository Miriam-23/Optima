from rest_framework import viewsets, mixins
from django.contrib.auth.models import User
from .models import Rol
from .serializers import UserSerializer, RolSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

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