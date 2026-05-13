from django import forms
from django.forms import inlineformset_factory
from django.db.models import Q
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


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['titulo', 'fecha', 'duracion_min', 'rutina', 'notas']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'notas': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, usuario=None, **kwargs):
        super().__init__(*args, **kwargs)
        if usuario:
            self.fields['rutina'].queryset = Rutina.objects.filter(usuario=usuario)
        self.fields['rutina'].required = False
        self.fields['titulo'].required = False


SerieFormSet = inlineformset_factory(
    WorkoutEjercicio,
    Serie,
    fields=['tipo', 'peso_kg', 'repeticiones'],
    extra=1,
    can_delete=True,
)


class WorkoutEjercicioForm(forms.ModelForm):
    class Meta:
        model = WorkoutEjercicio
        fields = ['ejercicio', 'notas']
        widgets = {
            'notas': forms.TextInput(attrs={'placeholder': 'Notas opcionales'}),
        }

    def __init__(self, *args, usuario=None, **kwargs):
        super().__init__(*args, **kwargs)
        if usuario:
            self.fields['ejercicio'].queryset = Ejercicio.objects.filter(
                Q(usuario=usuario) | Q(usuario__isnull=True)
            )


class SerieForm(forms.ModelForm):
    class Meta:
        model = Serie
        fields = ['tipo', 'peso_kg', 'repeticiones']
