from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.models import User, Group, Permission
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django import forms
from .forms import CustomUserCreationForm, CustomLoginForm, CustomUserUpdateForm
from django.contrib.auth.views import LoginView, LogoutView
from simple_history.models import HistoricalRecords
from people_management.models import Person, Contract
from itertools import chain
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from people_management.mixins import RoleRequiredMixin
from django.contrib import messages


class CustomPasswordResetCompleteView(RoleRequiredMixin, PasswordResetCompleteView):
    template_name = 'security/auth/password_reset_complete.html'
    allowed_roles = ['hr_admin']
    

class CustomPasswordResetConfirmView(RoleRequiredMixin, PasswordResetConfirmView):
    template_name = 'security/auth/password_reset_confirm.html'
    allowed_roles = ['hr_admin']

class CustomPasswordResetDoneView(RoleRequiredMixin, PasswordResetDoneView):
    template_name = 'security/auth/password_reset_done.html'
    allowed_roles = ['hr_admin']

class CustomPasswordResetView(RoleRequiredMixin, PasswordResetView):
    template_name = 'security/auth/password_reset.html'
    allowed_roles = ['hr_admin']


class LoginInterface(LoginView):
    """Handles user login."""
    form_class = CustomLoginForm
    template_name = "security/auth/login.html"

    def form_valid(self, form):
        messages.info(self.request, "You have logged in Succesfully!")
        return super().form_valid(form)


class LogoutInterface(LogoutView):
    """Handles user logout."""
    next_page = reverse_lazy("security:login")

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "You have been logged out.")
        return super().dispatch(request, *args, **kwargs)


# User Management Views
class ListUsers(RoleRequiredMixin, ListView):
    """Displays a list of users."""
    allowed_roles = ['hr_admin']
    model = User
    context_object_name = "users"
    template_name = "security/users/list.html"


class ViewUserDetails(RoleRequiredMixin, DetailView):
    """Displays details of a user."""
    allowed_roles = ['hr_admin']
    model = User
    context_object_name = "user"
    template_name = "security/users/detail.html"


class CreateNewUser(RoleRequiredMixin, CreateView):
    """Allows HR Admin to create a new user."""
    allowed_roles = ['hr_admin']
    model = User
    form_class = CustomUserCreationForm
    template_name = "security/users/form.html"
    success_url = reverse_lazy("security:user_list")
    
    def form_valid(self, form):
        """Ensures user is properly linked and password is auto-generated."""
        user = form.save(commit=False)
        user.is_staff = True
        user.save()
        return super().form_valid(form)


class UpdateUser(RoleRequiredMixin, UpdateView):
    """Allows HR Admin to update user information."""
    allowed_roles = ['hr_admin']
    model = User
    form_class = CustomUserUpdateForm
    template_name = "security/users/form.html"
    success_url = reverse_lazy("security:user_list")


class DeleteUser(RoleRequiredMixin, DeleteView):
    """Allows HR Admin to delete a user."""
    allowed_roles = ['hr_admin']
    model = User
    template_name = "security/users/confirm_delete.html"
    success_url = reverse_lazy("security:user_list")


# Group Management Forms
class GroupForm(RoleRequiredMixin, forms.ModelForm):
    """Form for creating and editing groups with permissions."""
    allowed_roles = ['hr_admin']
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Group
        fields = ["name", "permissions"]


# Group Management Views
class ListGroups(RoleRequiredMixin, PermissionRequiredMixin, ListView):
    """Displays a list of groups."""
    allowed_roles = ['hr_admin']
    model = Group
    context_object_name = "groups"
    template_name = "security/groups/list.html"
    permission_required = "auth.view_group"


class GroupDetailView(RoleRequiredMixin, PermissionRequiredMixin, DetailView):
    """Displays details of a group."""
    allowed_roles = ['hr_admin']
    model = Group
    template_name = "security/groups/detail.html"
    context_object_name = "group"
    permission_required = "auth.view_group"


class CreateGroup(RoleRequiredMixin, PermissionRequiredMixin, CreateView):
    """Allows authorized users to create a new group."""
    allowed_roles = ['hr_admin']
    model = Group
    form_class = GroupForm
    template_name = "security/groups/form.html"
    success_url = reverse_lazy("security:group_list")
    permission_required = "auth.add_group"


class UpdateGroup(RoleRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Allows authorized users to edit an existing group."""
    allowed_roles = ['hr_admin']
    model = Group
    form_class = GroupForm
    template_name = "security/groups/form.html"
    success_url = reverse_lazy("security:group_list")
    permission_required = "auth.change_group"


class DeleteGroup(RoleRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Allows authorized users to delete a group."""
    allowed_roles = ['hr_admin']
    model = Group
    template_name = "security/groups/confirm_delete.html"
    success_url = reverse_lazy("security:group_list")
    permission_required = "auth.delete_group"


class AuditLogListView(RoleRequiredMixin, ListView):
    allowed_roles = ['hr_admin']
    template_name = 'security/audit_log.html'
    context_object_name = 'audit_entries'

    def get_queryset(self):
        # Get history querysets for each model
        person_history = Person.history.all()
        contract_history = Contract.history.all()

        # Add model name to each historical record dynamically
        for entry in person_history:
            entry.model_name = entry.instance.__class__.__name__
        for entry in contract_history:
            entry.model_name = entry.instance.__class__.__name__ 

        # Combine both querysets
        combined_history = sorted(
            chain(person_history, contract_history),
            key=lambda entry: entry.history_date,
            reverse=True
        )

        # Return combined queryset
        return combined_history[:100]
