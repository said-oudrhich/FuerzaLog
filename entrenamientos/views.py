from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms

from .models import Entrenamiento, Rutina


class EntrenamientoListView(LoginRequiredMixin, ListView):
    model = Entrenamiento
    template_name = 'entrenamientos/lista_entrenamientos.html'
    context_object_name = 'entrenamientos'

    def get_queryset(self):
        return Entrenamiento.objects.filter(usuario=self.request.user)


class EntrenamientoDetailView(LoginRequiredMixin, DetailView):
    model = Entrenamiento
    template_name = 'entrenamientos/detalle_entrenamiento.html'


@login_required
def entrenamiento_create(request):
    if request.method == 'POST':
        form = EntrenamientoForm(request.POST, request.FILES)
        if form.is_valid():
            entrenamiento = form.save(commit=False)
            entrenamiento.usuario = request.user
            entrenamiento.save()
            messages.success(request, 'Entrenamiento creado.')
            return redirect('entrenamiento_list')
    else:
        form = EntrenamientoForm()
    return render(request, 'entrenamientos/formulario_entrenamiento.html', {'form': form})


@login_required
def entrenamiento_update(request, pk):
    entrenamiento = get_object_or_404(Entrenamiento, pk=pk)
    if entrenamiento.usuario != request.user and not request.user.is_staff:
        messages.error(request, 'No puedes editar esto.')
        return redirect('entrenamiento_list')
    if request.method == 'POST':
        form = EntrenamientoForm(request.POST, request.FILES, instance=entrenamiento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entrenamiento actualizado.')
            return redirect('entrenamiento_list')
    else:
        form = EntrenamientoForm(instance=entrenamiento)
    return render(request, 'entrenamientos/formulario_entrenamiento.html', {'form': form})


@login_required
def entrenamiento_delete(request, pk):
    entrenamiento = get_object_or_404(Entrenamiento, pk=pk)
    if entrenamiento.usuario != request.user and not request.user.is_staff:
        messages.error(request, 'No puedes borrar esto.')
        return redirect('entrenamiento_list')
    if request.method == 'POST':
        entrenamiento.delete()
        messages.success(request, 'Entrenamiento eliminado.')
        return redirect('entrenamiento_list')
    return render(request, 'entrenamientos/confirmar_eliminacion.html', {'entrenamiento': entrenamiento})


def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cuenta creada correctamente.')
            return redirect('entrenamiento_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def inicio(request):
    return render(request, 'inicio.html')


@login_required
def buscar(request):
    query = request.GET.get('q', '')
    entrenamientos = Entrenamiento.objects.filter(usuario=request.user)
    if query:
        entrenamientos = entrenamientos.filter(titulo__icontains=query)
    return render(request, 'entrenamientos/lista_entrenamientos.html', {'entrenamientos': entrenamientos})


class EntrenamientoForm(forms.ModelForm):
    class Meta:
        model = Entrenamiento
        fields = ['titulo', 'descripcion', 'peso', 'series', 'repeticiones', 'imagen', 'grupo_muscular', 'rutina']


class RutinaForm(forms.ModelForm):
    class Meta:
        model = Rutina
        fields = ['nombre', 'descripcion']


class RutinaListView(LoginRequiredMixin, ListView):
    model = Rutina
    template_name = 'entrenamientos/lista_rutinas.html'
    context_object_name = 'rutinas'

    def get_queryset(self):
        return Rutina.objects.filter(usuario=self.request.user)


@login_required
def rutina_create(request):
    if request.method == 'POST':
        form = RutinaForm(request.POST)
        if form.is_valid():
            rutina = form.save(commit=False)
            rutina.usuario = request.user
            rutina.save()
            messages.success(request, 'Rutina creada.')
            return redirect('rutina_list')
    else:
        form = RutinaForm()
    return render(request, 'entrenamientos/formulario_rutina.html', {'form': form})


@login_required
def rutina_update(request, pk):
    rutina = get_object_or_404(Rutina, pk=pk)
    if rutina.usuario != request.user and not request.user.is_staff:
        messages.error(request, 'No puedes editar esto.')
        return redirect('rutina_list')
    if request.method == 'POST':
        form = RutinaForm(request.POST, instance=rutina)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rutina actualizada.')
            return redirect('rutina_list')
    else:
        form = RutinaForm(instance=rutina)
    return render(request, 'entrenamientos/formulario_rutina.html', {'form': form})


@login_required
def rutina_delete(request, pk):
    rutina = get_object_or_404(Rutina, pk=pk)
    if rutina.usuario != request.user and not request.user.is_staff:
        messages.error(request, 'No puedes borrar esto.')
        return redirect('rutina_list')
    if request.method == 'POST':
        rutina.delete()
        messages.success(request, 'Rutina eliminada.')
        return redirect('rutina_list')
    return render(request, 'entrenamientos/confirmar_eliminacion_rutina.html', {'rutina': rutina})

