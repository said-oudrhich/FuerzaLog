from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .models import Ejercicio, Rutina, RutinaEjercicio, SerieRutina, Workout, WorkoutEjercicio, Serie
from .forms import EjercicioForm, RutinaForm, RutinaEjercicioForm, SerieRutinaForm, WorkoutForm, WorkoutEjercicioForm, SerieForm



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
            .order_by('-workout_ejercicio__workout__fecha')[:20]
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
        context['form_ejercicio'] = RutinaEjercicioForm()
        context['form_serie'] = SerieRutinaForm()
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


@login_required
def rutina_ejercicio_anadir(request, rutina_pk):
    rutina = get_object_or_404(Rutina, pk=rutina_pk, usuario=request.user)
    if request.method == 'POST':
        form = RutinaEjercicioForm(request.POST)
        if form.is_valid():
            bloque = form.save(commit=False)
            bloque.rutina = rutina
            bloque.orden = rutina.ejercicios.count()
            bloque.save()
            messages.success(request, 'Ejercicio añadido a la rutina.')
        else:
            messages.error(request, 'Elige un ejercicio válido.')
    return redirect('rutina_detail', pk=rutina_pk)


@login_required
def rutina_ejercicio_borrar(request, pk):
    bloque = get_object_or_404(RutinaEjercicio, pk=pk, rutina__usuario=request.user)
    rutina_pk = bloque.rutina.pk
    if request.method == 'POST':
        bloque.delete()
    return redirect('rutina_detail', pk=rutina_pk)


@login_required
def rutina_serie_crear(request, bloque_pk):
    bloque = get_object_or_404(RutinaEjercicio, pk=bloque_pk, rutina__usuario=request.user)
    if request.method == 'POST':
        form = SerieRutinaForm(request.POST)
        if form.is_valid():
            serie = form.save(commit=False)
            serie.rutina_ejercicio = bloque
            serie.save()
    return redirect('rutina_detail', pk=bloque.rutina.pk)


@login_required
def rutina_serie_borrar(request, pk):
    serie = get_object_or_404(SerieRutina, pk=pk, rutina_ejercicio__rutina__usuario=request.user)
    rutina_pk = serie.rutina_ejercicio.rutina.pk
    if request.method == 'POST':
        serie.delete()
    return redirect('rutina_detail', pk=rutina_pk)


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
        context['form_ejercicio'] = WorkoutEjercicioForm()
        context['form_serie'] = SerieForm()
        return context

    def test_func(self):
        return self.get_object().usuario == self.request.user or self.request.user.is_staff


class WorkoutCreateView(LoginRequiredMixin, CreateView):
    model = Workout
    form_class = WorkoutForm
    template_name = 'entrenamientos/formulario_workout.html'

    def get_initial(self):
        initial = super().get_initial()
        rutina_id = self.request.GET.get('rutina')
        if rutina_id:
            initial['rutina'] = rutina_id
        return initial

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        respuesta = super().form_valid(form)
        if self.object.rutina:
            for bloque_rutina in self.object.rutina.ejercicios.all():
                bloque_workout = WorkoutEjercicio.objects.create(
                    workout=self.object,
                    ejercicio=bloque_rutina.ejercicio,
                    orden=bloque_rutina.orden,
                    notas=bloque_rutina.notas,
                )
                # Genera series vacías según el número definido en la rutina
                num = bloque_rutina.series.first()
                cantidad = num.num_series if num else 3
                for i in range(cantidad):
                    Serie.objects.create(
                        workout_ejercicio=bloque_workout,
                        orden=i,
                    )
        messages.success(self.request, 'Entrenamiento creado.')
        return respuesta

    def get_success_url(self):
        return reverse('workout_detail', kwargs={'pk': self.object.pk})


class WorkoutUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Workout
    form_class = WorkoutForm
    template_name = 'entrenamientos/formulario_workout.html'
    success_url = reverse_lazy('workout_list')

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

@login_required
def ejercicio_anadir(request, workout_pk):
    workout = get_object_or_404(Workout, pk=workout_pk, usuario=request.user)
    if request.method == 'POST':
        form = WorkoutEjercicioForm(request.POST)
        if form.is_valid():
            bloque = form.save(commit=False)
            bloque.workout = workout
            bloque.orden = workout.ejercicios.count()
            bloque.save()
            messages.success(request, 'Ejercicio añadido.')
        else:
            messages.error(request, 'Elige un ejercicio válido.')
    return redirect('workout_detail', pk=workout_pk)


@login_required
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


@login_required
def serie_borrar(request, pk):
    serie = get_object_or_404(Serie, pk=pk, workout_ejercicio__workout__usuario=request.user)
    workout_pk = serie.workout_ejercicio.workout.pk
    if request.method == 'POST':
        serie.delete()
    return redirect('workout_detail', pk=workout_pk)


@login_required
def bloque_borrar(request, pk):
    bloque = get_object_or_404(WorkoutEjercicio, pk=pk, workout__usuario=request.user)
    workout_pk = bloque.workout.pk
    if request.method == 'POST':
        bloque.delete()
    return redirect('workout_detail', pk=workout_pk)

