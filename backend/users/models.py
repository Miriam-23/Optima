from django.db import models
# Importaremos el User estándar de Django más adelante cuando armemos las relaciones
# from django.contrib.auth.models import User 

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

