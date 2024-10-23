from django.shortcuts import render
from people_management.models import Person
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied 
from .forms import CustomUserCreationForm

class SignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'dashboard/register.html'
    success_url = '/'

    def form_valid(self, form):
        user = form.save(commit=False) 
        user.is_staff = form.cleaned_data.get('is_staff') 
        user.save()
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('dashboard')
        if not request.user.is_staff:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class LoginInterface(LoginView):
    template_name = 'dashboard/login.html'

class LogoutInterface(LogoutView):
    template_name = 'dashboard/logout.html'

class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    people = Person.objects.all()
    template_name = 'dashboard/dashboard.html'
    extra_context = {'people': people}


    