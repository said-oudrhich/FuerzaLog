from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect

from .models import Entrenamiento, Rutina
from .forms import EntrenamientoForm, RutinaForm


class EntrenamientoListView(LoginRequiredMixin, ListView):
    model = Entrenamiento
    template_name = 'entrenamientos/lista_entrenamientos.html'
    context_object_name = 'entrenamientos'

    def get_queryset(self):
        qs = Entrenamiento.objects.filter(usuario=self.request.user)
        query = self.request.GET.get('q', '')
        if query:
            qs = qs.filter(Q(titulo__icontains=query) | Q(descripcion__icontains=query))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class EntrenamientoDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Entrenamiento
    template_name = 'entrenamientos/detalle_entrenamiento.html'

    def test_func(self):
        return self.get_object().usuario == self.request.user or self.request.user.is_staff


class EntrenamientoCreateView(LoginRequiredMixin, CreateView):
    model = Entrenamiento
    form_class = EntrenamientoForm
    template_name = 'entrenamientos/formulario_entrenamiento.html'
    success_url = reverse_lazy('entrenamiento_list')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, 'Entrenamiento creado.')
        return super().form_valid(form)


class EntrenamientoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Entrenamiento
    form_class = EntrenamientoForm
    template_name = 'entrenamientos/formulario_entrenamiento.html'
    success_url = reverse_lazy('entrenamiento_list')

    def form_valid(self, form):
        messages.success(self.request, 'Entrenamiento actualizado.')
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().usuario == self.request.user or self.request.user.is_staff


class EntrenamientoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Entrenamiento
    template_name = 'entrenamientos/confirmar_eliminacion.html'
    context_object_name = 'entrenamiento'
    success_url = reverse_lazy('entrenamiento_list')

    def form_valid(self, form):
        messages.success(self.request, 'Entrenamiento eliminado.')
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().usuario == self.request.user or self.request.user.is_staff


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


class RutinaListView(LoginRequiredMixin, ListView):
    model = Rutina
    template_name = 'entrenamientos/lista_rutinas.html'
    context_object_name = 'rutinas'

    def get_queryset(self):
        return Rutina.objects.filter(usuario=self.request.user)


class RutinaCreateView(LoginRequiredMixin, CreateView):
    model = Rutina
    form_class = RutinaForm
    template_name = 'entrenamientos/formulario_rutina.html'
    success_url = reverse_lazy('rutina_list')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, 'Rutina creada.')
        return super().form_valid(form)


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
    template_name = 'entrenamientos/confirmar_eliminacion_rutina.html'
    context_object_name = 'rutina'
    success_url = reverse_lazy('rutina_list')

    def form_valid(self, form):
        messages.success(self.request, 'Rutina eliminada.')
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().usuario == self.request.user or self.request.user.is_staff

