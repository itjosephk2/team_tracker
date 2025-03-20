from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

from .forms import PersonForm, ContractForm
from people_management.models import Person, Contract
from people_management.filters import ContractFilter


# Person Views
class ListPeople(ListView):
    """
    Displays a list of Person objects with an optional filter for active/inactive status.

    If a 'status' GET parameter is provided ('active' or 'inactive'),
    the queryset is filtered accordingly.
    """
    model = Person
    context_object_name = 'people'

    def get_queryset(self):
        """
        Overrides the default queryset to filter by the 'status' GET parameter.
        """
        queryset = super().get_queryset().prefetch_related('contracts')
        status = self.request.GET.get('status')
        if status:
            if status.lower() == 'active':
                queryset = queryset.filter(active=True)
            elif status.lower() == 'inactive':
                queryset = queryset.filter(active=False)
        return queryset


class ViewPersonDetails(DetailView):
    """
    Displays detailed information for a single Person.
    """
    model = Person
    context_object_name = 'person'


class CreateNewPerson(CreateView):
    """
    Provides a form to create a new Person and redirects to the list view on success.
    """
    model = Person
    form_class = PersonForm
    success_url = reverse_lazy('people_management:people')


class UpdatePerson(UpdateView):
    """
    Provides a form to update an existing Person and redirects to the list view on success.
    """
    model = Person
    form_class = PersonForm
    success_url = reverse_lazy('people_management:people')


class DeletePerson(DeleteView):
    """
    Provides confirmation for deleting a Person and redirects to the list view on success.
    """
    model = Person
    success_url = reverse_lazy('people_management:people')


# Contract Views
class FilteredContractListView(FilterView):
    """
    Displays a list of Contract objects with filtering capabilities using django-filters.
    """
    model = Contract
    filterset_class = ContractFilter
    template_name = 'people_management/contract_list.html'
    context_object_name = 'contracts'


class ViewContractDetails(DetailView):
    """
    Displays detailed information for a single Contract.
    """
    model = Contract
    context_object_name = 'contract'


class CreateNewContract(CreateView):
    """
    Provides a form to create a new Contract and redirects to the list view on success.
    """
    model = Contract
    form_class = ContractForm
    success_url = reverse_lazy('people_management:contracts')


class UpdateContract(UpdateView):
    """
    Provides a form to update an existing Contract and redirects to the list view on success.
    """
    model = Contract
    form_class = ContractForm
    success_url = reverse_lazy('people_management:contracts')


class DeleteContract(DeleteView):
    """
    Provides confirmation for deleting a Contract and redirects to the list view on success.
    """
    model = Contract
    success_url = reverse_lazy('people_management:contracts')
