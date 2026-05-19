from django.contrib import admin
from .models import GrupoMuscular, Ejercicio, Rutina, RutinaEjercicio, SerieRutina, Entrenamiento, EntrenamientoEjercicio, Serie


admin.site.register(GrupoMuscular)
admin.site.register(Ejercicio)
admin.site.register(Rutina)
admin.site.register(RutinaEjercicio)
admin.site.register(SerieRutina)
admin.site.register(Entrenamiento)
admin.site.register(EntrenamientoEjercicio)
admin.site.register(Serie)
