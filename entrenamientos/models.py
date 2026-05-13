from django.contrib.auth.models import User
from django.db import models


class GrupoMuscular(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class Rutina(models.Model):
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Entrenamiento(models.Model):
    titulo = models.CharField(max_length=140)
    descripcion = models.TextField(blank=True)
    peso = models.PositiveIntegerField(null=True, blank=True)
    series = models.PositiveIntegerField()
    repeticiones = models.PositiveIntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='imagenes_entrenamientos/', blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    grupo_muscular = models.ForeignKey(GrupoMuscular, on_delete=models.PROTECT)
    rutina = models.ForeignKey(Rutina, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.titulo
