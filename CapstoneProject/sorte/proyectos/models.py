from django.db import models
from users.models import CustomUSer

# Create your models here.
class Proyecto(models.Model):
    imagen_proyecto = models.ImageField(null=True, blank=True, upload_to="proyectos")
    nombre_proyecto = models.CharField(max_length=100)
    descripcion = models.TextField()
    requisitos = models.TextField()
    cupos_disponibles_proyecto = models.IntegerField(default=30)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    fecha_creacion_proyecto = models.DateTimeField(auto_now_add=True)
    fecha_actualización_proyecto = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "proyecto"
        verbose_name_plural = "proyectos"

    def __str__(self):
        return self.nombre_proyecto
    
# Añadiendo un modelo para las solicitudes de postulación
class Solicitud(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    miembro = models.ForeignKey(CustomUSer, on_delete=models.CASCADE)
    ESTADO_CHOICES = (
    ('pendiente', 'Pendiente'),
    ('aceptada', 'Aceptada'),
    ('rechazada', 'Rechazada'),
    )
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Solicitud de {self.miembro.username} para {self.proyecto.nombre_proyecto}"