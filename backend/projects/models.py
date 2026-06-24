from django.db import models
from django.contrib.auth.models import User
from users.models import Rol  # Importamos el catálogo de Roles

# ENTIDAD PROYECTO
class Proyecto(models.Model):
    # Usamos TextChoices para mantener la base de datos limpia sin tablas extra
    class EstadoGeneral(models.TextChoices):
        PLANIFICACION = 'Planificacion', 'Planificación'
        EN_PROGRESO = 'En progreso', 'En progreso'
        COMPLETADO = 'Completado', 'Completado'
        PAUSADO = 'Pausado', 'Pausado'

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    estado_general = models.CharField(
        max_length=20,
        choices=EstadoGeneral.choices,
        default=EstadoGeneral.PLANIFICACION
    )

    class Meta:
        db_table = 'proyectos'
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'

    def __str__(self):
        return self.nombre

# ENTIDAD RELACIONAL (Asignación de Usuarios a Proyectos)
class ProyectoUsuario(models.Model):
    # related_name='proyectos_asignados' permitirá buscar fácilmente: usuario.proyectos_asignados.all()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proyectos_asignados')
    
    # related_name='equipo' permitirá buscar fácilmente: proyecto.equipo.all()
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='equipo')
    
    # on_delete=models.PROTECT evita que alguien borre un Rol si hay usuarios usándolo
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT) 
    
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'proyecto_usuario'
        verbose_name = 'Asignación de Proyecto'
        verbose_name_plural = 'Asignaciones de Proyectos'
        
        # Esto evita asignar al mismo usuario con el mismo rol dos veces en el mismo proyecto
        unique_together = ('usuario', 'proyecto', 'rol') 

    def __str__(self):
        # El User estándar de Django usa 'username' por defecto en sus consultas
        return f"{self.usuario.username} -> {self.proyecto.nombre} ({self.rol.nombre})"