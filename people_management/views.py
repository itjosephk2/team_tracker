from typing import List
from django.shortcuts import render
from django.http import Http404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy

from .forms import PersonForm
from people_management.models import Person, Contract

# Person Views
class ListPeople(ListView):
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

class DeletePerson(DeleteView):
    model = Person
    success_url = reverse_lazy('people')

# Contract Views
class ListContracts(ListView):
    model = Contract
    context_object_name = 'contract'

class ViewContractDetails(DetailView):
    model = Contract
    context_object_name = 'contract'

class CreateNewContract(CreateView):
    model = Contract
    success_url = reverse_lazy('contracts')
    form_class = PersonForm

class UpdateContract(UpdateView):
    model = Contract
    success_url = reverse_lazy('contracts')
    form_class = PersonForm

class DeteContract(DeleteView):
    model = Contract
    success_url = reverse_lazy('contracts')