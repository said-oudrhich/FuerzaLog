from django.urls import path
from . import views

urlpatterns = [
    path('', views.EntrenamientoListView.as_view(), name='entrenamiento_list'),
    path('entrenamiento/<int:pk>/', views.EntrenamientoDetailView.as_view(), name='entrenamiento_detail'),
    path('entrenamiento/nuevo/', views.entrenamiento_create, name='entrenamiento_create'),
    path('entrenamiento/<int:pk>/editar/', views.entrenamiento_update, name='entrenamiento_update'),
    path('entrenamiento/<int:pk>/eliminar/', views.entrenamiento_delete, name='entrenamiento_delete'),
    path('registro/', views.registro, name='registro'),
    path('buscar/', views.buscar, name='buscar'),
    path('rutinas/', views.RutinaListView.as_view(), name='rutina_list'),
    path('rutina/nueva/', views.rutina_create, name='rutina_create'),
    path('rutina/<int:pk>/editar/', views.rutina_update, name='rutina_update'),
    path('rutina/<int:pk>/eliminar/', views.rutina_delete, name='rutina_delete'),
]

