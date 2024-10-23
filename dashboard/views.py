from django.shortcuts import render
from people_management.models import Person
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

# Create your views here.
class DashboardView(TemplateView):
    people = Person.objects.all()
    template_name = 'dashboard/dashboard.html'
    extra_context = {'people': people}

class AuthorizedView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/authorized.html'

    