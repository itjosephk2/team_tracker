from typing import List
from django.shortcuts import render
from django.http import Http404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy

from .forms import PersonForm
from people_management.models import Person

# Create your views here.
class ListPeopleView(ListView):
    model = Person
    context_object_name = 'people'
    template_name = 'people_management/list_people.html'

class ViewPersonDetails(DetailView):
    model = Person
    context_object_name = 'person'
    template_name = 'people_management/view_person.html'

class CreateNewPerson(CreateView):
    model = Person
    template_name = 'people_management/create_person.html'
    success_url = reverse_lazy('people')
    form_class = PersonForm

class UpdatePerson(UpdateView):
    model = Person
    template_name = 'people_management/create_person.html'
    success_url = reverse_lazy('people')
    form_class = PersonForm