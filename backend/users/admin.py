from django.contrib import admin
from .models import Rol

# Register your models here.
admin.site.register(Rol)
# Nota: No registramos al 'Usuario' porque Django ya lo incluye por defecto.