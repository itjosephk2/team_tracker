from typing import List
from django.shortcuts import render
from django.http import Http404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy

from .forms import PersonForm
from people_management.models import Person

# Create your views here.
class ListPeopleView(ListView):
    model = Person
    context_object_name = 'people'

class ViewPersonDetails(DetailView):
    model = Person
    context_object_name = 'person'

class CreateNewPerson(CreateView):
    model = Person
    success_url = reverse_lazy('people')
    form_class = PersonForm

class UpdatePerson(UpdateView):
    model = Person
    success_url = reverse_lazy('people')
    form_class = PersonForm

class DetePerson(DeleteView):
    model = Person
    success_url = reverse_lazy('people')