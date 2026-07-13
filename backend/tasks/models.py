from django.db import models
from django.contrib.auth.models import User
from projects.models import Proyecto  # Importamos Proyecto para la llave foránea

# CATÁLOGO DE ESTADOS
class Estado(models.Model):
    # Permite estados dinámicos como 'Pendiente', 'En progreso', 'Bloqueado', 'Completado'
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'estados'
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'

    def __str__(self):
        return self.nombre

# ENTIDAD TAREA (El Core Operacional)
class Tarea(models.Model):
    # Choices internos para optimizar la prioridad sin tablas extra
    class Prioridad(models.TextChoices):
        ALTA = 'Alta', 'Alta'
        MEDIA = 'Media', 'Media'
        BAJA = 'Baja', 'Baja'

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_limite = models.DateField()
    fecha_finalizacion_real = models.DateField(blank=True, null=True)
    
    # Campo clave para el dashboard de carga de trabajo de los miembros
    esfuerzo_estimado = models.PositiveIntegerField(
        help_text="Esfuerzo estimado en horas o puntos de historia",
        blank=True, 
        null=True
    )
    
    prioridad = models.CharField(
        max_length=10,
        choices=Prioridad.choices,
        default=Prioridad.MEDIA
    )

    # Relaciones y llaves foráneas
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='tareas')
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT, related_name='tareas')

    class Meta:
        db_table = 'tareas'
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'

    def __str__(self):
        return self.titulo

# ENTIDAD RELACIONAL (Asignación de Múltiples Responsables a Tareas)
class TareaUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tareas_asignadas')
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='responsables')
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tarea_usuario'
        verbose_name = 'Responsable de Tarea'
        verbose_name_plural = 'Responsables de Tareas'
        # Candado estructural: Evita duplicar al mismo usuario en la misma tarea
        unique_together = ('usuario', 'tarea')

    def __str__(self):
        return f"{self.usuario.username} -> {self.tarea.titulo}"

# 4. MODULO DE COMENTARIOS
class Comentario(models.Model):
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comentarios')
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='comentarios')

    class Meta:
        db_table = 'comentarios'
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'

    def __str__(self):
        return f"Comentario de {self.usuario.username} en {self.tarea.titulo}"

# TABLA DE AUDITORÍA (Dormida estructuralmente por estrategia de tiempo)
class HistorialTarea(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='historial')
    # Usamos SET_NULL para que si un usuario se borra, el registro del historial no se pierda
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='historial_cambios')
    cambio_realizado = models.TextField()
    fecha_cambio = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'historial_tareas'
        verbose_name = 'Historial de Tarea'
        verbose_name_plural = 'Historiales de Tareas'

    def __str__(self):
        return f"Cambio en {self.tarea.titulo} el {self.fecha_cambio}"