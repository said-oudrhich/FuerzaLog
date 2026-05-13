from django import forms
from .models import Entrenamiento, Rutina


class EntrenamientoForm(forms.ModelForm):
    class Meta:
        model = Entrenamiento
        fields = ['titulo', 'descripcion', 'peso', 'series', 'repeticiones', 'imagen', 'grupo_muscular', 'rutina']


class RutinaForm(forms.ModelForm):
    class Meta:
        model = Rutina
        fields = ['nombre', 'descripcion']
