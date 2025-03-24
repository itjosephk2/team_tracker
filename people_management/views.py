from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import PersonForm, ContractForm
from people_management.models import Person, Contract
from people_management.filters import ContractFilter
from django.contrib import messages
from django.shortcuts import get_object_or_404


# Person Views
class ListPeople(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Person
    context_object_name = 'people'
    permission_required = 'people_management.view_person'

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('contracts')
        status = self.request.GET.get('status')
        if status:
            if status.lower() == 'active':
                queryset = queryset.filter(active=True)
            elif status.lower() == 'inactive':
                queryset = queryset.filter(active=False)
        return queryset


class ViewPersonDetails(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Person
    context_object_name = 'person'
    permission_required = 'people_management.view_person'


class ViewOwnPerson(LoginRequiredMixin, DetailView):
    model = Person
    template_name = 'people_management/person_detail.html'
    context_object_name = 'person'

    def get_object(self):
        return get_object_or_404(Person, user=self.request.user)


class CreateNewPerson(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Person
    form_class = PersonForm
    permission_required = 'people_management.add_person'
    success_url = reverse_lazy('people_management:people')

    def form_valid(self, form):
        messages.success(self.request, "Person created successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid submission error!")
        return super().form_invalid(form)


class UpdatePerson(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Person
    form_class = PersonForm
    permission_required = 'people_management.change_person'
    success_url = reverse_lazy('people_management:people')

    def form_valid(self, form):
        messages.success(self.request, "Person Updated Successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid submission error!")
        return super().form_invalid(form)


class DeletePerson(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Person
    permission_required = 'people_management.delete_person'
    success_url = reverse_lazy('people_management:people')

    def form_valid(self, form):
        messages.success(self.request, "Person successfully Deleted!")
        return super().form_valid(form)


# Contract Views
class FilteredContractListView(LoginRequiredMixin, PermissionRequiredMixin, FilterView):
    model = Contract
    filterset_class = ContractFilter
    permission_required = 'people_management.view_contract'
    template_name = 'people_management/contract_list.html'
    context_object_name = 'contracts'


class ViewContractDetails(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Contract
    context_object_name = 'contract'
    permission_required = 'people_management.view_contract'


class CreateNewContract(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Contract
    form_class = ContractForm
    permission_required = 'people_management.add_contract'
    success_url = reverse_lazy('people_management:contracts')

    def form_valid(self, form):
        messages.success(self.request, "Contract created successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid submission error!")
        return super().form_invalid(form)


class UpdateContract(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Contract
    form_class = ContractForm
    permission_required = 'people_management.change_contract'
    success_url = reverse_lazy('people_management:contracts')

    def form_valid(self, form):
        messages.success(self.request, "Contract successfully updated!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid submission error!")
        return super().form_invalid(form)


class DeleteContract(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Contract
    permission_required = 'people_management.delete_contract'
    success_url = reverse_lazy('people_management:contracts')

    def form_valid(self, form):
        messages.success(self.request, "Contract successfully Deleted!")
        return super().form_valid(form)