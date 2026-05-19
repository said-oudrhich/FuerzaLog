from django.contrib import admin
from .models import GrupoMuscular, Ejercicio, Rutina, RutinaEjercicio, SerieRutina, Entrenamiento, EntrenamientoEjercicio, Serie


admin.site.site_header = 'Administración de FuerzaLog'
admin.site.site_title = 'FuerzaLog'
admin.site.index_title = 'Panel de administración'


@admin.register(GrupoMuscular)
class GrupoMuscularAdmin(admin.ModelAdmin):
    search_fields = ['nombre']
    ordering = ['nombre']


@admin.register(Ejercicio)
class EjercicioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'grupo_muscular', 'usuario', 'fecha_creacion']
    list_filter = ['grupo_muscular', 'usuario']
    search_fields = ['nombre', 'descripcion']
    autocomplete_fields = ['grupo_muscular', 'usuario']
    ordering = ['grupo_muscular__nombre', 'nombre']


class SerieRutinaInline(admin.TabularInline):
    model = SerieRutina
    extra = 0


class RutinaEjercicioInline(admin.TabularInline):
    model = RutinaEjercicio
    extra = 0
    autocomplete_fields = ['ejercicio']


@admin.register(Rutina)
class RutinaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'usuario', 'fecha_creacion']
    list_filter = ['usuario']
    search_fields = ['nombre', 'descripcion']
    autocomplete_fields = ['usuario']
    inlines = [RutinaEjercicioInline]


@admin.register(RutinaEjercicio)
class RutinaEjercicioAdmin(admin.ModelAdmin):
    list_display = ['rutina', 'ejercicio', 'orden', 'notas']
    list_filter = ['rutina']
    search_fields = ['rutina__nombre', 'ejercicio__nombre', 'notas']
    autocomplete_fields = ['rutina', 'ejercicio']
    inlines = [SerieRutinaInline]


@admin.register(SerieRutina)
class SerieRutinaAdmin(admin.ModelAdmin):
    list_display = ['rutina_ejercicio', 'num_series']
    autocomplete_fields = ['rutina_ejercicio']


class EntrenamientoEjercicioInline(admin.TabularInline):
    model = EntrenamientoEjercicio
    extra = 0
    autocomplete_fields = ['ejercicio']


class SerieInline(admin.TabularInline):
    model = Serie
    extra = 0


@admin.register(Entrenamiento)
class EntrenamientoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'fecha', 'usuario', 'rutina']
    list_filter = ['fecha', 'usuario', 'rutina']
    search_fields = ['nombre', 'descripcion']
    autocomplete_fields = ['usuario', 'rutina']
    date_hierarchy = 'fecha'
    inlines = [EntrenamientoEjercicioInline]


@admin.register(EntrenamientoEjercicio)
class EntrenamientoEjercicioAdmin(admin.ModelAdmin):
    list_display = ['entrenamiento', 'ejercicio', 'orden', 'notas']
    list_filter = ['entrenamiento']
    search_fields = ['entrenamiento__nombre', 'ejercicio__nombre', 'notas']
    autocomplete_fields = ['entrenamiento', 'ejercicio']
    inlines = [SerieInline]


@admin.register(Serie)
class SerieAdmin(admin.ModelAdmin):
    list_display = ['entrenamiento_ejercicio', 'tipo', 'peso_kg', 'repeticiones', 'orden']
    list_filter = ['tipo']
    search_fields = ['entrenamiento_ejercicio__ejercicio__nombre']
    autocomplete_fields = ['entrenamiento_ejercicio']
