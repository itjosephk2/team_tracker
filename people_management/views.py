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
from functools import wraps
from django.shortcuts import redirect
from django.utils.decorators import method_decorator


def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if hasattr(request.user, 'employee'):
                user_role = request.user.employee.role
                if user_role in allowed_roles:
                    return view_func(request, *args, **kwargs)
            # Redirect to a custom 403 page
            return redirect('403_page')  # Ensure you have a URL pattern named '403_page'
        return _wrapped_view
    return decorator


# Person Views
class ListPeople(ListView):
    model = Person
    context_object_name = 'people'


class ViewPersonDetails(DetailView):
    model = Person
    context_object_name = 'person'

# @method_decorator(role_required(['manager', 'hr_admin']), name='dispatch')
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
