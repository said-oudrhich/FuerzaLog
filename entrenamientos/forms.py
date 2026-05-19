from django import forms
from django.db.models import Q
from .models import Ejercicio, Rutina, RutinaEjercicio, SerieRutina, Entrenamiento, EntrenamientoEjercicio, Serie


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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['ejercicio'].queryset = Ejercicio.objects.filter(
                Q(usuario=user) | Q(usuario__isnull=True)
            )


class SerieRutinaForm(forms.ModelForm):
    class Meta:
        model = SerieRutina
        fields = ['num_series']


class EntrenamientoForm(forms.ModelForm):
    class Meta:
        model = Entrenamiento
        fields = ['nombre', 'fecha', 'rutina', 'descripcion']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['rutina'].required = False
        self.fields['nombre'].required = False
        if user is not None:
            self.fields['rutina'].queryset = Rutina.objects.filter(usuario=user)


class EntrenamientoEjercicioForm(forms.ModelForm):
    class Meta:
        model = EntrenamientoEjercicio
        fields = ['ejercicio', 'notas']
        widgets = {
            'notas': forms.TextInput(attrs={'placeholder': 'Notas opcionales'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['ejercicio'].queryset = Ejercicio.objects.filter(
                Q(usuario=user) | Q(usuario__isnull=True)
            )


class SerieForm(forms.ModelForm):
    class Meta:
        model = Serie
        fields = ['tipo', 'peso_kg', 'repeticiones']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select form-select-sm'}),
        }
