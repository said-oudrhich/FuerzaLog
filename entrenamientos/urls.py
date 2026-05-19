from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),

    # Ejercicios
    path('ejercicio/', views.EjercicioListView.as_view(), name='ejercicio_list'),
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

    # Acciones dentro del detalle de rutina
    path('rutina/<int:rutina_pk>/ejercicio/anadir/', views.rutina_ejercicio_anadir, name='rutina_ejercicio_anadir'),
    path('rutina-bloque/<int:pk>/borrar/', views.rutina_ejercicio_borrar, name='rutina_ejercicio_borrar'),
    path('rutina-bloque/<int:bloque_pk>/serie/nueva/', views.rutina_serie_crear, name='rutina_serie_crear'),
    path('rutina-serie/<int:pk>/borrar/', views.rutina_serie_borrar, name='rutina_serie_borrar'),

    # Entrenamientos
    path('entrenamientos/', views.EntrenamientoListView.as_view(), name='entrenamiento_list'),
    path('entrenamiento/<int:pk>/', views.EntrenamientoDetailView.as_view(), name='entrenamiento_detail'),
    path('entrenamiento/nuevo/', views.EntrenamientoCreateView.as_view(), name='entrenamiento_create'),
    path('entrenamiento/<int:pk>/editar/', views.EntrenamientoUpdateView.as_view(), name='entrenamiento_update'),
    path('entrenamiento/<int:pk>/eliminar/', views.EntrenamientoDeleteView.as_view(), name='entrenamiento_delete'),

    # Acciones dentro del detalle de entrenamiento
    path('entrenamiento/<int:entrenamiento_pk>/ejercicio/anadir/', views.ejercicio_anadir, name='ejercicio_anadir'),
    path('bloque/<int:bloque_pk>/serie/nueva/', views.serie_crear, name='serie_crear'),
    path('serie/<int:pk>/borrar/', views.serie_borrar, name='serie_borrar'),
    path('bloque/<int:pk>/borrar/', views.bloque_borrar, name='bloque_borrar'),
]

