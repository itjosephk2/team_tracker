from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .forms import UserForm  # Assuming you have a UserForm for user creation
from security.models import Role, PermissionDefinition
from security.forms import RoleForm  # Assuming you have a RoleForm for role management


class HRAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin to restrict access to HR Admin users only.
    Ensures that the logged-in user has an associated `Person` object
    and their assigned role is 'HR Admin'.
    """

    def test_func(self):
        """Check if the logged-in user is an HR Admin."""
        return hasattr(self.request.user, "employee") and self.request.user.employee.role.name == "HR Admin"

    def handle_no_permission(self):
        """Raise permission denied if user is not authorized."""
        raise PermissionDenied("You do not have permission to access this page.")


#Users
class ListUsers(LoginRequiredMixin, ListView):
    """
    View to list all registered users.
    Requires authentication.
    """
    model = User
    context_object_name = "users"
    template_name = "security/user_list.html"  # Update to match your template structure


class ViewUserDetails(LoginRequiredMixin, DetailView):
    """
    View to display details of a specific user.
    Requires authentication.
    """
    model = User
    context_object_name = "user"
    template_name = "security/user_detail.html"  # Update to match your template structure


class CreateNewUser(HRAdminRequiredMixin, CreateView):
    """
    View to create a new user.
    Restricted to HR Admins only.
    """
    model = User
    form_class = UserForm
    success_url = reverse_lazy("security:user_list")  # Redirect to user list after creation
    template_name = "auth/user_form.html"


class UpdateUser(HRAdminRequiredMixin, UpdateView):
    """
    View to update user details.
    Restricted to HR Admins only.
    """
    model = User
    form_class = UserForm
    success_url = reverse_lazy("security:user_list")  # Redirect to user list after update
    template_name = "security/user_form.html"


class DeleteUser(HRAdminRequiredMixin, DeleteView):
    """
    View to delete a user.
    Restricted to HR Admins only.
    """
    model = User
    success_url = reverse_lazy("security:user_list")  # Redirect to user list after deletion
    template_name = "security/user_confirm_delete.html"



# Roles
class ListRoles(HRAdminRequiredMixin, ListView):
    """
    View to list all available roles.
    Restricted to HR Admins only.
    """
    model = Role
    context_object_name = "roles"
    template_name = "security/role_list.html"


class ViewRoleDetails(HRAdminRequiredMixin, DetailView):
    """
    View to display details of a specific role.
    Restricted to HR Admins only.
    """
    model = Role
    context_object_name = "role"
    template_name = "security/role_detail.html"


class CreateNewRole(HRAdminRequiredMixin, CreateView):
    """
    View to create a new role.
    Restricted to HR Admins only.
    """
    model = Role
    form_class = RoleForm
    success_url = reverse_lazy("security:role_list")
    template_name = "security/role_form.html"

    def form_valid(self, form):
        """Add a success message after role creation."""
        messages.success(self.request, "New role created successfully!")
        return super().form_valid(form)


class UpdateRole(HRAdminRequiredMixin, UpdateView):
    """
    View to update an existing role.
    Restricted to HR Admins only.
    """
    model = Role
    form_class = RoleForm
    success_url = reverse_lazy("security:role_list")
    template_name = "security/role_form.html"

    def form_valid(self, form):
        """Add a success message after role update."""
        messages.success(self.request, "Role updated successfully!")
        return super().form_valid(form)


class DeleteRole(HRAdminRequiredMixin, DeleteView):
    """
    View to delete a role.
    Restricted to HR Admins only.
    """
    model = Role
    success_url = reverse_lazy("security:role_list")
    template_name = "security/role_confirm_delete.html"

    def delete(self, request, *args, **kwargs):
        """Add a success message after role deletion."""
        messages.success(self.request, "Role deleted successfully!")
        return super().delete(request, *args, **kwargs)


# =======================
# ✅ ROLE PERMISSION MANAGEMENT
# =======================

# @login_required
def role_permissions(request, role_id):
    """
    View to manage permissions assigned to a role.
    Restricted to HR Admins only.
    """
    role = get_object_or_404(Role, id=role_id)

    if request.method == "POST":
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            messages.success(request, "Permissions updated successfully!")
            return redirect("security:role_list")
    else:
        form = RoleForm(instance=role)

    return render(request, "security/role_permissions.html", {"form": form, "role": role})