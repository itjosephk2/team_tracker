from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import UserForm  # Form for user creation and updates


class ListUsers(LoginRequiredMixin, ListView):
    """
    Displays a list of all registered users.
    Requires authentication.
    """
    model = User
    context_object_name = "users"
    template_name = "security/user_list.html"  # Ensure this template exists


class ViewUserDetails(LoginRequiredMixin, DetailView):
    """
    Displays details of a specific user.
    Requires authentication.
    """
    model = User
    context_object_name = "user"
    template_name = "security/user_detail.html"  # Ensure this template exists


class CreateNewUser(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Allows HR Admins to create a new user.
    Access is restricted to HR Admins only.
    """
    model = User
    form_class = UserForm
    template_name = "security/user_form.html"
    success_url = reverse_lazy("security:user_list")

    def test_func(self):
        """Restricts access to HR Admins."""
        return self.request.user.groups.filter(name="HR Admin").exists()


class UpdateUser(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allows HR Admins to update user details.
    Access is restricted to HR Admins only.
    """
    model = User
    form_class = UserForm
    template_name = "security/user_form.html"
    success_url = reverse_lazy("security:user_list")

    def test_func(self):
        """Restricts access to HR Admins."""
        return self.request.user.groups.filter(name="HR Admin").exists()


class DeleteUser(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Allows HR Admins to delete a user.
    Access is restricted to HR Admins only.
    """
    model = User
    template_name = "security/user_confirm_delete.html"
    success_url = reverse_lazy("security:user_list")

    def test_func(self):
        """Restricts access to HR Admins."""
        return self.request.user.groups.filter(name="HR Admin").exists()
