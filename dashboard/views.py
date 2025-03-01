from django.shortcuts import render, redirect
from people_management.models import Person
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy  # Added import
from .forms import CustomUserCreationForm, CustomLoginForm


class SignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'dashboard/register.html'
    success_url = reverse_lazy('login')  # Changed to reverse_lazy for dynamic URL resolution

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_staff = form.cleaned_data.get('is_staff')
        user.save()
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')  # Redirect logged-in users to the dashboard
        return super().dispatch(request, *args, **kwargs)


class LoginInterface(LoginView):
    form_class = CustomLoginForm
    template_name = 'dashboard/login.html'


class LogoutInterface(LogoutView):
    next_page = '/login/'  # Redirects to login after logout


class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['people'] = Person.objects.all()  # Fetch people here for every request
        return context
