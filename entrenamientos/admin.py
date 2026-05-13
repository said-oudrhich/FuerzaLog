from django.contrib import admin
from .models import Entrenamiento, GrupoMuscular, Rutina

admin.site.register(GrupoMuscular)
admin.site.register(Rutina)
admin.site.register(Entrenamiento)
