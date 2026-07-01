from django.contrib import admin
from .models import Estado, Tarea, TareaUsuario, Comentario

# Register your models here.
admin.site.register(Estado)
admin.site.register(Tarea)
admin.site.register(TareaUsuario)
admin.site.register(Comentario)