from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import RoleRequiredMixin
from .forms import PersonForm, ContractForm
from people_management.models import Person, Contract
from people_management.filters import ContractFilter
from django.contrib import messages
from django.shortcuts import get_object_or_404


# Person Views
class ListPeople(RoleRequiredMixin, ListView):
    """
    Displays a list of Person objects with an optional filter for active/inactive status.

    If a 'status' GET parameter is provided ('active' or 'inactive'),
    the queryset is filtered accordingly.
    """
    model = Person
    context_object_name = 'people'
    allowed_roles = ['manager', 'hr_admin']

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


class ViewPersonDetails(RoleRequiredMixin, DetailView):
    """
    Displays detailed information for a single Person.
    """
    model = Person
    context_object_name = 'person'
    allowed_roles = ['manager', 'hr_admin']


class ViewOwnPerson(LoginRequiredMixin, DetailView):
    model = Person
    template_name = 'people_management/person_detail.html'
    context_object_name = 'person'

    def get_object(self):
        return get_object_or_404(Person, user=self.request.user)


class CreateNewPerson(RoleRequiredMixin, CreateView):
    """
    Provides a form to create a new Person and redirects to the list view on success.
    """
    model = Person
    form_class = PersonForm
    allowed_roles = ['manager', 'hr_admin']
    success_url = reverse_lazy('people_management:people')

    def form_valid(self, form):
        messages.success(self.request, "Person created successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid submission error!")
        return super().form_invalid(form)
    

class UpdatePerson(RoleRequiredMixin, UpdateView):
    """
    Provides a form to update an existing Person and redirects to the list view on success.
    """
    model = Person
    form_class = PersonForm
    allowed_roles = ['manager', 'hr_admin']
    success_url = reverse_lazy('people_management:people')

    def form_valid(self, form):
        messages.success(self.request, "Person Updated Succesfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid submission error!")
        return super().form_invalid(form)
    

class DeletePerson(RoleRequiredMixin, DeleteView):
    """
    Provides confirmation for deleting a Person and redirects to the list view on success.
    """
    model = Person
    allowed_roles = ['manager', 'hr_admin']
    success_url = reverse_lazy('people_management:people')

    def form_valid(self, form):
        messages.success(self.request, "Person succesfully Deleted!")
        return super().form_valid(form)
    

# Contract Views
class FilteredContractListView(RoleRequiredMixin, FilterView):
    """
    Displays a list of Contract objects with filtering capabilities using django-filters.
    """
    model = Contract
    filterset_class = ContractFilter
    allowed_roles = ['manager', 'hr_admin']
    template_name = 'people_management/contract_list.html'
    context_object_name = 'contracts'


class ViewContractDetails(RoleRequiredMixin, DetailView):
    """
    Displays detailed information for a single Contract.
    """
    model = Contract
    context_object_name = 'contract'
    allowed_roles = ['manager', 'hr_admin']


class CreateNewContract(RoleRequiredMixin, CreateView):
    """
    Provides a form to create a new Contract and redirects to the list view on success.
    """
    model = Contract
    form_class = ContractForm
    allowed_roles = ['manager', 'hr_admin']
    success_url = reverse_lazy('people_management:contracts')

    def form_valid(self, form):
        messages.success(self.request, "Contract created successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid submission error!")
        return super().form_invalid(form)

    
class UpdateContract(RoleRequiredMixin, UpdateView):
    """
    Provides a form to update an existing Contract and redirects to the list view on success.
    """
    model = Contract
    form_class = ContractForm
    allowed_roles = ['manager', 'hr_admin']
    success_url = reverse_lazy('people_management:contracts')

    def form_valid(self, form):
        messages.success(self.request, "Contract successfully updated!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid submission error!")
        return super().form_invalid(form)


class DeleteContract(RoleRequiredMixin, DeleteView):
    """
    Provides confirmation for deleting a Contract and redirects to the list view on success.
    """
    model = Contract
    allowed_roles = ['manager', 'hr_admin']
    success_url = reverse_lazy('people_management:contracts')

    def form_valid(self, form):
        messages.success(self.request, "Contract succesfully Deleted!")
        return super().form_valid(form)
