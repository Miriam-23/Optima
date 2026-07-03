from django.db import models
from django.contrib.auth.models import User

class Notificacion(models.Model):
    class TipoNotificacion(models.TextChoices):
        TAREA_ASIGNADA = 'tarea_asignada', 'Tarea asignada'
        COMENTARIO_NUEVO = 'comentario_nuevo', 'Comentario nuevo'
        TAREA_VENCIDA = 'tarea_vencida', 'Tarea vencida'
        MIEMBRO_AGREGADO = 'miembro_agregado', 'Miembro agregado al proyecto'

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones')
    tipo = models.CharField(max_length=50, choices=TipoNotificacion.choices)
    mensaje = models.TextField()
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notificaciones'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.usuario.username} — {self.tipo}"