from django.contrib import admin
from .models import GrupoMuscular, Ejercicio, Rutina, RutinaEjercicio, SerieRutina, Workout, WorkoutEjercicio, Serie


@admin.register(GrupoMuscular)
class GrupoMuscularAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    ordering = ['nombre']


@admin.register(Ejercicio)
class EjercicioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'grupo_muscular', 'usuario']
    list_filter = ['grupo_muscular']
    search_fields = ['nombre']


class SerieRutinaInline(admin.TabularInline):
    model = SerieRutina
    extra = 1


class RutinaEjercicioInline(admin.TabularInline):
    model = RutinaEjercicio
    extra = 1


@admin.register(Rutina)
class RutinaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'usuario', 'fecha_creacion']
    inlines = [RutinaEjercicioInline]


class SerieInline(admin.TabularInline):
    model = Serie
    extra = 0


class WorkoutEjercicioInline(admin.TabularInline):
    model = WorkoutEjercicio
    extra = 0


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'fecha', 'usuario', 'rutina']
    list_filter = ['usuario']
    inlines = [WorkoutEjercicioInline]
