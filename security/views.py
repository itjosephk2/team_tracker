from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .forms import UserForm  # Assuming you have these forms

class HRAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin that only allows access if the logged-in user is an HR Admin.
    """
    def test_func(self):
        # Check that the user has an employee profile and that their role is 'hr_admin'
        return hasattr(self.request.user, 'employee') and self.request.user.employee.role == "hr_admin"
    
    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to access this page.")


# User Views
class ListUsers(ListView):
    model = User
    context_object_name = 'users'


class ViewUserDetails(DetailView):
    model = User
    context_object_name = 'user'


class CreateNewUser(CreateView):
    model = User
    form_class = UserForm  # Custom form for user creation
    success_url = reverse_lazy('users')  # Redirect to user list after successful creation


class UpdateUser(UpdateView):
    model = User
    form_class = UserForm  # Custom form for user updating
    success_url = reverse_lazy('users')  # Redirect to user list after successful update


class DeleteUser(DeleteView):
    model = User
    success_url = reverse_lazy('users')  # Redirect to user list after deletion
