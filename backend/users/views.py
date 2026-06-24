from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import Rol
from .serializers import UserSerializer, RolSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_active=True) # Solo enviamos usuarios activos
    serializer_class = UserSerializer

class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer