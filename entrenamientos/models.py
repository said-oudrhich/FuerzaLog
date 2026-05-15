from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class GrupoMuscular(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class Ejercicio(models.Model):
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    grupo_muscular = models.ForeignKey(GrupoMuscular, on_delete=models.PROTECT)
    imagen = models.ImageField(upload_to='ejercicios/', blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['grupo_muscular__nombre', 'nombre']

    def __str__(self):
        return self.nombre


class Rutina(models.Model):
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rutinas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class RutinaEjercicio(models.Model):
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE, related_name='ejercicios')
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.PROTECT)
    orden = models.PositiveIntegerField(default=0)
    notas = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return f"{self.ejercicio.nombre} ({self.rutina.nombre})"


class SerieRutina(models.Model):
    rutina_ejercicio = models.ForeignKey(RutinaEjercicio, on_delete=models.CASCADE, related_name='series')
    num_series = models.PositiveIntegerField(default=3)

    def __str__(self):
        return f"{self.num_series} serie(s)"


class Workout(models.Model):
    nombre = models.CharField(max_length=120, blank=True)
    descripcion = models.TextField(blank=True)
    fecha = models.DateField(default=timezone.now)
    rutina = models.ForeignKey(
        Rutina, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='workouts'
    )
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workouts')

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return self.nombre or f"Entrenamiento {self.fecha}"


class WorkoutEjercicio(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='ejercicios')
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.PROTECT)
    orden = models.PositiveIntegerField(default=0)
    notas = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return f"{self.ejercicio.nombre}"


class Serie(models.Model):
    TIPOS = [
        ('N', 'Normal'),
        ('W', 'Calentamiento'),
        ('F', 'Al fallo'),
    ]
    workout_ejercicio = models.ForeignKey(WorkoutEjercicio, on_delete=models.CASCADE, related_name='series')
    tipo = models.CharField(max_length=1, choices=TIPOS, default='N')
    peso_kg = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    repeticiones = models.PositiveIntegerField(default=0)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        peso = f"{self.peso_kg}kg x " if self.peso_kg else ""
        return f"{self.get_tipo_display()}: {peso}{self.repeticiones} reps"
