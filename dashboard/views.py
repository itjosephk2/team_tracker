from django.shortcuts import render
from people_management.models import Person
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView

# Create your views here.
class LoginInterface(LoginView):
    template_name = 'dashboard/login.html'

class LogoutInterface(LogoutView):
    template_name = 'dashboard/logout.html'

class DashboardView(TemplateView):
    people = Person.objects.all()
    template_name = 'dashboard/dashboard.html'
    extra_context = {'people': people}

class AuthorizedView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/authorized.html'

    