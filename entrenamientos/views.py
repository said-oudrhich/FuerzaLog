from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .models import Ejercicio, Rutina, RutinaEjercicio, Workout, WorkoutEjercicio, Serie
from .forms import EjercicioForm, RutinaForm, WorkoutForm, WorkoutEjercicioForm, SerieForm, SerieFormSet


def inicio(request):
    return render(request, 'inicio.html')


def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cuenta creada.')
            return redirect('workout_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


# ── Ejercicios ────────────────────────────────────────────────

class EjercicioListView(LoginRequiredMixin, ListView):
    model = Ejercicio
    template_name = 'entrenamientos/lista_ejercicios.html'
    context_object_name = 'ejercicios'

    def get_queryset(self):
        qs = Ejercicio.objects.filter(
            Q(usuario=self.request.user) | Q(usuario__isnull=True)
        ).select_related('grupo_muscular')
        q = self.request.GET.get('q', '')
        if q:
            qs = qs.filter(nombre__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class EjercicioDetailView(LoginRequiredMixin, DetailView):
    model = Ejercicio
    template_name = 'entrenamientos/detalle_ejercicio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['historial'] = (
            Serie.objects
            .filter(
                workout_ejercicio__ejercicio=self.object,
                workout_ejercicio__workout__usuario=self.request.user
            )
            .select_related('workout_ejercicio__workout')
            .order_by('-workout_ejercicio__workout__fecha')[:30]
        )
        return context


class EjercicioCreateView(LoginRequiredMixin, CreateView):
    model = Ejercicio
    form_class = EjercicioForm
    template_name = 'entrenamientos/formulario_ejercicio.html'
    success_url = reverse_lazy('ejercicio_list')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, 'Ejercicio creado.')
        return super().form_valid(form)


class EjercicioUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ejercicio
    form_class = EjercicioForm
    template_name = 'entrenamientos/formulario_ejercicio.html'
    success_url = reverse_lazy('ejercicio_list')

    def form_valid(self, form):
        messages.success(self.request, 'Ejercicio actualizado.')
        return super().form_valid(form)

    def test_func(self):
        obj = self.get_object()
        return obj.usuario == self.request.user or self.request.user.is_staff


class EjercicioDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ejercicio
    template_name = 'entrenamientos/confirmar_eliminacion.html'
    context_object_name = 'objeto'
    success_url = reverse_lazy('ejercicio_list')

    def form_valid(self, form):
        messages.success(self.request, 'Ejercicio eliminado.')
        return super().form_valid(form)

    def test_func(self):
        obj = self.get_object()
        return obj.usuario == self.request.user or self.request.user.is_staff


# ── Rutinas ───────────────────────────────────────────────────

class RutinaListView(LoginRequiredMixin, ListView):
    model = Rutina
    template_name = 'entrenamientos/lista_rutinas.html'
    context_object_name = 'rutinas'

    def get_queryset(self):
        return Rutina.objects.filter(usuario=self.request.user)


class RutinaDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Rutina
    template_name = 'entrenamientos/detalle_rutina.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ejercicios'] = self.object.ejercicios.select_related('ejercicio').prefetch_related('series')
        return context

    def test_func(self):
        return self.get_object().usuario == self.request.user or self.request.user.is_staff


class RutinaCreateView(LoginRequiredMixin, CreateView):
    model = Rutina
    form_class = RutinaForm
    template_name = 'entrenamientos/formulario_rutina.html'
    success_url = reverse_lazy('rutina_list')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, 'Rutina creada.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('rutina_detail', kwargs={'pk': self.object.pk})


class RutinaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Rutina
    form_class = RutinaForm
    template_name = 'entrenamientos/formulario_rutina.html'
    success_url = reverse_lazy('rutina_list')

    def form_valid(self, form):
        messages.success(self.request, 'Rutina actualizada.')
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().usuario == self.request.user or self.request.user.is_staff


class RutinaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Rutina
    template_name = 'entrenamientos/confirmar_eliminacion.html'
    context_object_name = 'objeto'
    success_url = reverse_lazy('rutina_list')

    def form_valid(self, form):
        messages.success(self.request, 'Rutina eliminada.')
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().usuario == self.request.user or self.request.user.is_staff


# ── Workouts ──────────────────────────────────────────────────

class WorkoutListView(LoginRequiredMixin, ListView):
    model = Workout
    template_name = 'entrenamientos/lista_workouts.html'
    context_object_name = 'workouts'

    def get_queryset(self):
        return Workout.objects.filter(usuario=self.request.user).select_related('rutina')


class WorkoutDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Workout
    template_name = 'entrenamientos/detalle_workout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bloques'] = (
            self.object.ejercicios
            .select_related('ejercicio__grupo_muscular')
            .prefetch_related('series')
        )
        context['form_ejercicio'] = WorkoutEjercicioForm(usuario=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = WorkoutEjercicioForm(request.POST, usuario=request.user)
        if form.is_valid():
            bloque = form.save(commit=False)
            bloque.workout = self.object
            bloque.orden = self.object.ejercicios.count()
            bloque.save()
            messages.success(request, 'Ejercicio añadido.')
        else:
            messages.error(request, 'Elige un ejercicio válido.')
        return redirect('workout_detail', pk=self.object.pk)

    def test_func(self):
        return self.get_object().usuario == self.request.user or self.request.user.is_staff


class WorkoutCreateView(LoginRequiredMixin, CreateView):
    model = Workout
    form_class = WorkoutForm
    template_name = 'entrenamientos/formulario_workout.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['usuario'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, 'Entrenamiento creado.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('workout_detail', kwargs={'pk': self.object.pk})


class WorkoutUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Workout
    form_class = WorkoutForm
    template_name = 'entrenamientos/formulario_workout.html'
    success_url = reverse_lazy('workout_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['usuario'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Entrenamiento actualizado.')
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().usuario == self.request.user or self.request.user.is_staff


class WorkoutDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Workout
    template_name = 'entrenamientos/confirmar_eliminacion.html'
    context_object_name = 'objeto'
    success_url = reverse_lazy('workout_list')

    def form_valid(self, form):
        messages.success(self.request, 'Entrenamiento eliminado.')
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().usuario == self.request.user or self.request.user.is_staff


# ── Series dentro de un bloque ───────────────────────────────

def serie_crear(request, bloque_pk):
    bloque = get_object_or_404(WorkoutEjercicio, pk=bloque_pk, workout__usuario=request.user)
    if request.method == 'POST':
        form = SerieForm(request.POST)
        if form.is_valid():
            serie = form.save(commit=False)
            serie.workout_ejercicio = bloque
            serie.orden = bloque.series.count()
            serie.save()
    return redirect('workout_detail', pk=bloque.workout.pk)


def serie_borrar(request, pk):
    serie = get_object_or_404(Serie, pk=pk, workout_ejercicio__workout__usuario=request.user)
    workout_pk = serie.workout_ejercicio.workout.pk
    if request.method == 'POST':
        serie.delete()
    return redirect('workout_detail', pk=workout_pk)


def bloque_borrar(request, pk):
    bloque = get_object_or_404(WorkoutEjercicio, pk=pk, workout__usuario=request.user)
    workout_pk = bloque.workout.pk
    if request.method == 'POST':
        bloque.delete()
    return redirect('workout_detail', pk=workout_pk)

