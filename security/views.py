from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
    PermissionRequiredMixin,
)
from django.contrib.auth.models import User, Group, Permission
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django import forms
from .forms import CustomUserCreationForm, CustomLoginForm, CustomUserUpdateForm
from django.contrib.auth.views import LoginView, LogoutView
from simple_history.models import HistoricalRecords
from people_management.models import Person, Contract
from itertools import chain
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.contrib import messages


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "security/auth/password_reset_complete.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "security/auth/password_reset_confirm.html"


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "security/auth/password_reset_done.html"


class CustomPasswordResetView(PasswordResetView):
    template_name = "security/auth/password_reset.html"


class LoginInterface(LoginView):
    """Handles user login."""

    form_class = CustomLoginForm
    template_name = "security/auth/login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("dashboard")

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
class ListUsers(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Displays a list of users."""

    model = User
    context_object_name = "users"
    template_name = "security/users/list.html"
    permission_required = "auth.view_user"


class ViewUserDetails(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Displays details of a user."""

    model = User
    context_object_name = "user"
    template_name = "security/users/detail.html"
    permission_required = "auth.view_user"


class CreateNewUser(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Allows HR Admin to create a new user."""

    model = User
    form_class = CustomUserCreationForm
    template_name = "security/users/form.html"
    success_url = reverse_lazy("security:user_list")
    permission_required = "auth.add_user"

    def form_valid(self, form):
        """Ensures user is properly linked and password is auto-generated."""
        user = form.save(commit=False)
        user.is_staff = True
        user.save()
        messages.success(self.request, "User successfully Created!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid submission error!")
        return super().form_invalid(form)


class UpdateUser(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Allows HR Admin to update user information."""

    model = User
    form_class = CustomUserUpdateForm
    template_name = "security/users/form.html"
    success_url = reverse_lazy("security:user_list")
    permission_required = "auth.change_user"

    def form_valid(self, form):
        messages.success(self.request, "User successfully Created!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid submission error!")
        return super().form_invalid(form)


class DeleteUser(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Allows HR Admin to delete a user."""

    model = User
    template_name = "security/users/confirm_delete.html"
    success_url = reverse_lazy("security:user_list")
    permission_required = "auth.delete_user"


# Group Management Forms
class GroupForm(forms.ModelForm):
    """Form for creating and editing groups with permissions."""

    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Group
        fields = ["name", "permissions"]


# Group Management Views
class ListGroups(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Displays a list of groups."""

    model = Group
    context_object_name = "groups"
    template_name = "security/groups/list.html"
    permission_required = "auth.view_group"


class GroupDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Displays details of a group."""

    model = Group
    template_name = "security/groups/detail.html"
    context_object_name = "group"
    permission_required = "auth.view_group"


class CreateGroup(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Allows authorized users to create a new group."""

    model = Group
    form_class = GroupForm
    template_name = "security/groups/form.html"
    success_url = reverse_lazy("security:group_list")
    permission_required = "auth.add_group"

    def form_valid(self, form):
        messages.success(self.request, "Group successfully Created!")
        return super().form_valid(form)


class UpdateGroup(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Allows authorized users to edit an existing group."""

    model = Group
    form_class = GroupForm
    template_name = "security/groups/form.html"
    success_url = reverse_lazy("security:group_list")
    permission_required = "auth.change_group"

    def form_valid(self, form):
        messages.success(self.request, "Group successfully Updated!")
        return super().form_valid(form)


class DeleteGroup(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Allows authorized users to delete a group."""

    model = Group
    template_name = "security/groups/confirm_delete.html"
    success_url = reverse_lazy("security:group_list")
    permission_required = "auth.delete_group"

    def form_valid(self, form):
        messages.warning(self.request, "Deleting Groups might break usability!")
        return super().form_valid(form)


class AuditLogListView(LoginRequiredMixin, ListView):
    template_name = "security/audit_log.html"
    context_object_name = "audit_entries"

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
            reverse=True,
        )

        # Return combined queryset
        return combined_history[:100]
