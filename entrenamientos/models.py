from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class GrupoMuscular(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class Ejercicio(models.Model):
    """Catálogo de ejercicios. Los globales los crea el admin; el usuario puede crear los suyos."""
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

    @property
    def es_personalizado(self):
        return self.usuario is not None


# ── Rutinas (plantillas) ──────────────────────────────────────

class Rutina(models.Model):
    """Plantilla de entrenamiento: lista de ejercicios con series objetivo."""
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class RutinaEjercicio(models.Model):
    """Un ejercicio dentro de una plantilla de rutina, con su orden."""
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE, related_name='ejercicios')
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.PROTECT)
    orden = models.PositiveIntegerField(default=0)
    notas = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return f"{self.ejercicio.nombre}"


class SerieRutina(models.Model):
    """Serie objetivo dentro de un RutinaEjercicio (plantilla)."""
    TIPOS = [
        ('normal', 'Normal'),
        ('calentamiento', 'Calentamiento'),
        ('fallo', 'Al fallo'),
    ]
    rutina_ejercicio = models.ForeignKey(RutinaEjercicio, on_delete=models.CASCADE, related_name='series')
    tipo = models.CharField(max_length=15, choices=TIPOS, default='normal')
    repeticiones = models.PositiveIntegerField(default=10)
    peso_kg = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return f"{self.tipo} — {self.repeticiones} reps"


# ── Workouts (entrenamientos reales) ─────────────────────────

class Workout(models.Model):
    """Entrenamiento realizado. Puede partir de una rutina o ser libre."""
    titulo = models.CharField(max_length=120, blank=True)
    fecha = models.DateField(default=timezone.now)
    duracion_min = models.PositiveIntegerField(null=True, blank=True)
    notas = models.TextField(blank=True)
    rutina = models.ForeignKey(
        Rutina, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='workouts'
    )
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return self.titulo or f"Entrenamiento {self.fecha}"


class WorkoutEjercicio(models.Model):
    """Bloque de un ejercicio dentro de un workout, con su orden."""
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='ejercicios')
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.PROTECT)
    orden = models.PositiveIntegerField(default=0)
    notas = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return f"{self.ejercicio.nombre}"


class Serie(models.Model):
    """Serie ejecutada dentro de un WorkoutEjercicio."""
    TIPOS = [
        ('normal', 'Normal'),
        ('calentamiento', 'Calentamiento'),
        ('fallo', 'Al fallo'),
    ]
    workout_ejercicio = models.ForeignKey(WorkoutEjercicio, on_delete=models.CASCADE, related_name='series')
    tipo = models.CharField(max_length=15, choices=TIPOS, default='normal')
    peso_kg = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    repeticiones = models.PositiveIntegerField()
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        peso = f"{self.peso_kg}kg x " if self.peso_kg else ""
        return f"{peso}{self.repeticiones} reps ({self.tipo})"
