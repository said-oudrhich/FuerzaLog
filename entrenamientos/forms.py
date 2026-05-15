from django import forms
from .models import Ejercicio, Rutina, RutinaEjercicio, SerieRutina, Workout, WorkoutEjercicio, Serie


class EjercicioForm(forms.ModelForm):
    class Meta:
        model = Ejercicio
        fields = ['nombre', 'descripcion', 'grupo_muscular', 'imagen']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }


class RutinaForm(forms.ModelForm):
    class Meta:
        model = Rutina
        fields = ['nombre', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }


class RutinaEjercicioForm(forms.ModelForm):
    class Meta:
        model = RutinaEjercicio
        fields = ['ejercicio', 'notas']
        widgets = {
            'notas': forms.TextInput(attrs={'placeholder': 'Notas opcionales'}),
        }


class SerieRutinaForm(forms.ModelForm):
    class Meta:
        model = SerieRutina
        fields = ['num_series']


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['nombre', 'fecha', 'rutina', 'descripcion']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rutina'].required = False
        self.fields['nombre'].required = False



class WorkoutEjercicioForm(forms.ModelForm):
    class Meta:
        model = WorkoutEjercicio
        fields = ['ejercicio', 'notas']
        widgets = {
            'notas': forms.TextInput(attrs={'placeholder': 'Notas opcionales'}),
        }


class SerieForm(forms.ModelForm):
    class Meta:
        model = Serie
        fields = ['tipo', 'peso_kg', 'repeticiones']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select form-select-sm'}),
        }
