from django.urls import path
from . import views

urlpatterns = [
    path('', views.EntrenamientoListView.as_view(), name='entrenamiento_list'),
    path('entrenamiento/<int:pk>/', views.EntrenamientoDetailView.as_view(), name='entrenamiento_detail'),
    path('entrenamiento/nuevo/', views.EntrenamientoCreateView.as_view(), name='entrenamiento_create'),
    path('entrenamiento/<int:pk>/editar/', views.EntrenamientoUpdateView.as_view(), name='entrenamiento_update'),
    path('entrenamiento/<int:pk>/eliminar/', views.EntrenamientoDeleteView.as_view(), name='entrenamiento_delete'),
    path('registro/', views.registro, name='registro'),
    path('buscar/', views.buscar, name='buscar'),
    path('rutinas/', views.RutinaListView.as_view(), name='rutina_list'),
    path('rutina/nueva/', views.rutina_create, name='rutina_create'),
    path('rutina/<int:pk>/editar/', views.rutina_update, name='rutina_update'),
    path('rutina/<int:pk>/eliminar/', views.rutina_delete, name='rutina_delete'),
]

