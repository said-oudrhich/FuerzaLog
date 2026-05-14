from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),

    # Ejercicios
    path('ejercicios/', views.EjercicioListView.as_view(), name='ejercicio_list'),
    path('ejercicio/<int:pk>/', views.EjercicioDetailView.as_view(), name='ejercicio_detail'),
    path('ejercicio/nuevo/', views.EjercicioCreateView.as_view(), name='ejercicio_create'),
    path('ejercicio/<int:pk>/editar/', views.EjercicioUpdateView.as_view(), name='ejercicio_update'),
    path('ejercicio/<int:pk>/eliminar/', views.EjercicioDeleteView.as_view(), name='ejercicio_delete'),

    # Rutinas
    path('rutinas/', views.RutinaListView.as_view(), name='rutina_list'),
    path('rutina/<int:pk>/', views.RutinaDetailView.as_view(), name='rutina_detail'),
    path('rutina/nueva/', views.RutinaCreateView.as_view(), name='rutina_create'),
    path('rutina/<int:pk>/editar/', views.RutinaUpdateView.as_view(), name='rutina_update'),
    path('rutina/<int:pk>/eliminar/', views.RutinaDeleteView.as_view(), name='rutina_delete'),

    # Workouts
    path('workouts/', views.WorkoutListView.as_view(), name='workout_list'),
    path('workout/<int:pk>/', views.WorkoutDetailView.as_view(), name='workout_detail'),
    path('workout/nuevo/', views.WorkoutCreateView.as_view(), name='workout_create'),
    path('workout/<int:pk>/editar/', views.WorkoutUpdateView.as_view(), name='workout_update'),
    path('workout/<int:pk>/eliminar/', views.WorkoutDeleteView.as_view(), name='workout_delete'),

    # Acciones dentro del detalle de workout
    path('workout/<int:workout_pk>/ejercicio/anadir/', views.ejercicio_anadir, name='ejercicio_anadir'),
    path('bloque/<int:bloque_pk>/serie/nueva/', views.serie_crear, name='serie_crear'),
    path('serie/<int:pk>/borrar/', views.serie_borrar, name='serie_borrar'),
    path('bloque/<int:pk>/borrar/', views.bloque_borrar, name='bloque_borrar'),
]

