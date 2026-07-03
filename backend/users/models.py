from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

# CATÁLOGO DE ROLES
class Rol(models.Model):
    # Definimos los roles que se asignarán dentro de un proyecto (Backend, Tester, etc.)
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'roles'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.nombre

class TokenVerificacion(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='token_verificacion')
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def ha_expirado(self):
        return timezone.now() > self.creado_en + timedelta(hours=24)

    class Meta:
        db_table = 'tokens_verificacion'