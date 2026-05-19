from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .models import Ejercicio, Rutina, RutinaEjercicio, SerieRutina, Entrenamiento, EntrenamientoEjercicio, Serie
from .forms import EjercicioForm, RutinaForm, RutinaEjercicioForm, SerieRutinaForm, EntrenamientoForm, EntrenamientoEjercicioForm, SerieForm


def inicio(request):
    return render(request, 'inicio.html')


def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cuenta creada.')
            return redirect('entrenamiento_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# Ejercicios

class EjercicioListView(LoginRequiredMixin, ListView):
    model = Ejercicio
    template_name = 'entrenamientos/lista_ejercicios.html'
    context_object_name = 'ejercicios'

    def get_queryset(self):
        # Asi se mezclan los ejercicios comunes con los del usuario, sin enseñar los de otra persona.
        qs = Ejercicio.objects.filter(
            Q(usuario=self.request.user) | Q(usuario__isnull=True)
        )
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
        context['historial'] = Serie.objects.filter(
            entrenamiento_ejercicio__ejercicio=self.object,
            entrenamiento_ejercicio__entrenamiento__usuario=self.request.user
        ).order_by('-entrenamiento_ejercicio__entrenamiento__fecha')[:20]
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
        ejercicio = self.get_object()
        return ejercicio.usuario == self.request.user or self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, 'No puedes modificar este elemento.')
        return redirect('ejercicio_list')


class EjercicioDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ejercicio
    template_name = 'entrenamientos/confirmar_eliminacion.html'
    context_object_name = 'objeto'
    success_url = reverse_lazy('ejercicio_list')

    def form_valid(self, form):
        messages.success(self.request, 'Ejercicio eliminado.')
        return super().form_valid(form)

    def test_func(self):
        ejercicio = self.get_object()
        return ejercicio.usuario == self.request.user or self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, 'No puedes modificar este elemento.')
        return redirect('ejercicio_list')

# Rutinas

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
        context['ejercicios'] = self.object.ejercicios.all()
        context['form_ejercicio'] = RutinaEjercicioForm(user=self.request.user)
        context['form_serie'] = SerieRutinaForm()
        return context

    def test_func(self):
        rutina = self.get_object()
        return rutina.usuario == self.request.user or self.request.user.is_staff


class RutinaCreateView(LoginRequiredMixin, CreateView):
    model = Rutina
    form_class = RutinaForm
    template_name = 'entrenamientos/formulario_rutina.html'

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
        rutina = self.get_object()
        return rutina.usuario == self.request.user or self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, 'No puedes modificar este elemento.')
        return redirect('rutina_list')


class RutinaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Rutina
    template_name = 'entrenamientos/confirmar_eliminacion.html'
    context_object_name = 'objeto'
    success_url = reverse_lazy('rutina_list')

    def form_valid(self, form):
        messages.success(self.request, 'Rutina eliminada.')
        return super().form_valid(form)

    def test_func(self):
        rutina = self.get_object()
        return rutina.usuario == self.request.user or self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, 'No puedes modificar este elemento.')
        return redirect('rutina_list')


@login_required
def rutina_ejercicio_anadir(request, rutina_pk):
    rutina = get_object_or_404(Rutina, pk=rutina_pk, usuario=request.user)
    if request.method == 'POST':
        form = RutinaEjercicioForm(request.POST, user=request.user)
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

# Entrenamientos

class EntrenamientoListView(LoginRequiredMixin, ListView):
    model = Entrenamiento
    template_name = 'entrenamientos/lista_entrenamientos.html'
    context_object_name = 'entrenamientos'

    def get_queryset(self):
        return Entrenamiento.objects.filter(usuario=self.request.user)


class EntrenamientoDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Entrenamiento
    template_name = 'entrenamientos/detalle_entrenamiento.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bloques'] = self.object.ejercicios.all()
        context['form_ejercicio'] = EntrenamientoEjercicioForm(user=self.request.user)
        context['form_serie'] = SerieForm()
        return context

    def test_func(self):
        entrenamiento = self.get_object()
        return entrenamiento.usuario == self.request.user or self.request.user.is_staff


class EntrenamientoCreateView(LoginRequiredMixin, CreateView):
    model = Entrenamiento
    form_class = EntrenamientoForm
    template_name = 'entrenamientos/formulario_entrenamiento.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        rutina_pk = self.request.GET.get('rutina')
        if rutina_pk:
            initial['rutina'] = get_object_or_404(Rutina, pk=rutina_pk, usuario=self.request.user)
        return initial

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        respuesta = super().form_valid(form)
        if self.object.rutina:
            for bloque_rutina in self.object.rutina.ejercicios.all():
                bloque_entrenamiento = EntrenamientoEjercicio.objects.create(
                    entrenamiento=self.object,
                    ejercicio=bloque_rutina.ejercicio,
                    orden=bloque_rutina.orden,
                    notas=bloque_rutina.notas,
                )
                num = bloque_rutina.series.first()
                cantidad = num.num_series if num else 3
                for i in range(cantidad):
                    Serie.objects.create(
                        entrenamiento_ejercicio=bloque_entrenamiento,
                        orden=i,
                    )
        messages.success(self.request, 'Entrenamiento creado.')
        return respuesta

    def get_success_url(self):
        return reverse('entrenamiento_detail', kwargs={'pk': self.object.pk})


class EntrenamientoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Entrenamiento
    form_class = EntrenamientoForm
    template_name = 'entrenamientos/formulario_entrenamiento.html'
    success_url = reverse_lazy('entrenamiento_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Entrenamiento actualizado.')
        return super().form_valid(form)

    def test_func(self):
        entrenamiento = self.get_object()
        return entrenamiento.usuario == self.request.user or self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, 'No puedes modificar este elemento.')
        return redirect('entrenamiento_list')


class EntrenamientoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Entrenamiento
    template_name = 'entrenamientos/confirmar_eliminacion.html'
    context_object_name = 'objeto'
    success_url = reverse_lazy('entrenamiento_list')

    def form_valid(self, form):
        messages.success(self.request, 'Entrenamiento eliminado.')
        return super().form_valid(form)

    def test_func(self):
        entrenamiento = self.get_object()
        return entrenamiento.usuario == self.request.user or self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, 'No puedes modificar este elemento.')
        return redirect('entrenamiento_list')

# Series dentro de un bloque

@login_required
def ejercicio_anadir(request, entrenamiento_pk):
    entrenamiento = get_object_or_404(Entrenamiento, pk=entrenamiento_pk, usuario=request.user)
    if request.method == 'POST':
        form = EntrenamientoEjercicioForm(request.POST, user=request.user)
        if form.is_valid():
            bloque = form.save(commit=False)
            bloque.entrenamiento = entrenamiento
            bloque.orden = entrenamiento.ejercicios.count()
            bloque.save()
            messages.success(request, 'Ejercicio añadido.')
        else:
            messages.error(request, 'Elige un ejercicio válido.')
    return redirect('entrenamiento_detail', pk=entrenamiento_pk)


@login_required
def serie_crear(request, bloque_pk):
    bloque = get_object_or_404(EntrenamientoEjercicio, pk=bloque_pk, entrenamiento__usuario=request.user)
    if request.method == 'POST':
        form = SerieForm(request.POST)
        if form.is_valid():
            serie = form.save(commit=False)
            serie.entrenamiento_ejercicio = bloque
            serie.orden = bloque.series.count()
            serie.save()
    return redirect('entrenamiento_detail', pk=bloque.entrenamiento.pk)


@login_required
def serie_borrar(request, pk):
    serie = get_object_or_404(Serie, pk=pk, entrenamiento_ejercicio__entrenamiento__usuario=request.user)
    entrenamiento_pk = serie.entrenamiento_ejercicio.entrenamiento.pk
    if request.method == 'POST':
        serie.delete()
    return redirect('entrenamiento_detail', pk=entrenamiento_pk)


@login_required
def bloque_borrar(request, pk):
    bloque = get_object_or_404(EntrenamientoEjercicio, pk=pk, entrenamiento__usuario=request.user)
    entrenamiento_pk = bloque.entrenamiento.pk
    if request.method == 'POST':
        bloque.delete()
    return redirect('entrenamiento_detail', pk=entrenamiento_pk)
