from django.contrib import admin
from .models import (
    GrupoMuscular,
    Ejercicio,
    Rutina,
    RutinaEjercicio,
    SerieRutina,
    Entrenamiento,
    EntrenamientoEjercicio,
    Serie,
)


admin.site.site_header = 'Administración de FuerzaLog'
admin.site.site_title = 'FuerzaLog'
admin.site.index_title = 'Panel de administración'


@admin.register(GrupoMuscular)
class GrupoMuscularAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']


@admin.register(Ejercicio)
class EjercicioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'grupo_muscular', 'usuario']
    list_filter = ['grupo_muscular']
    search_fields = ['nombre']


@admin.register(Rutina)
class RutinaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'usuario', 'fecha_creacion']
    search_fields = ['nombre']


@admin.register(RutinaEjercicio)
class RutinaEjercicioAdmin(admin.ModelAdmin):
    list_display = ['rutina', 'ejercicio', 'orden']


@admin.register(SerieRutina)
class SerieRutinaAdmin(admin.ModelAdmin):
    list_display = ['rutina_ejercicio', 'num_series']


@admin.register(Entrenamiento)
class EntrenamientoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'fecha', 'usuario', 'rutina']
    list_filter = ['fecha']
    search_fields = ['nombre']


@admin.register(EntrenamientoEjercicio)
class EntrenamientoEjercicioAdmin(admin.ModelAdmin):
    list_display = ['entrenamiento', 'ejercicio', 'orden']


@admin.register(Serie)
class SerieAdmin(admin.ModelAdmin):
    list_display = ['entrenamiento_ejercicio', 'tipo', 'peso_kg', 'repeticiones']
    list_filter = ['tipo']
