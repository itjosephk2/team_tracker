from typing import List
from django.shortcuts import render
from django.http import Http404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django_filters.views import FilterView
from .forms import PersonForm, ContractForm
from people_management.models import Person, Contract
from people_management.filters import ContractFilter


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
class FilteredContractListView(FilterView):
    model = Contract
    filterset_class = ContractFilter
    template_name = 'people_management/contract_list.html'
    context_object_name = 'contracts'


class ViewContractDetails(DetailView):
    model = Contract
    context_object_name = 'contract'


class CreateNewContract(CreateView):
    model = Contract
    success_url = reverse_lazy('contracts')
    form_class = ContractForm


class UpdateContract(UpdateView):
    model = Contract
    success_url = reverse_lazy('contracts')
    form_class = ContractForm


class DeleteContract(DeleteView):
    model = Contract
    success_url = reverse_lazy('contracts')
