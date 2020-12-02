from django.db import models
from uuid import uuid4

def content_file_name(instance, filename):
    name = f"{uuid4().hex}_{filename}"
    return '/'.join(['actividades', name])
    
class Actividad(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)
    instrucciones = models.TextField(max_length=3000)
    tipo = models.CharField(max_length=200)
    imagen = models.FileField(upload_to=content_file_name, default=None)

    def __str__(self):
        return self.nombre
    