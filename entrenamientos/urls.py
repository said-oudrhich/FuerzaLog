from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('entrenamientos/', views.EntrenamientoListView.as_view(), name='entrenamiento_list'),
    path('entrenamiento/<int:pk>/', views.EntrenamientoDetailView.as_view(), name='entrenamiento_detail'),
    path('entrenamiento/nuevo/', views.EntrenamientoCreateView.as_view(), name='entrenamiento_create'),
    path('entrenamiento/<int:pk>/editar/', views.EntrenamientoUpdateView.as_view(), name='entrenamiento_update'),
    path('entrenamiento/<int:pk>/eliminar/', views.EntrenamientoDeleteView.as_view(), name='entrenamiento_delete'),
    path('registro/', views.registro, name='registro'),
    path('rutinas/', views.RutinaListView.as_view(), name='rutina_list'),
    path('rutina/nueva/', views.RutinaCreateView.as_view(), name='rutina_create'),
    path('rutina/<int:pk>/editar/', views.RutinaUpdateView.as_view(), name='rutina_update'),
    path('rutina/<int:pk>/eliminar/', views.RutinaDeleteView.as_view(), name='rutina_delete'),
]

