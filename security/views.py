from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth.models import User, Group, Permission
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django import forms

from .forms import UserForm  # Form for user creation and updates


class ListUsers(LoginRequiredMixin, ListView):
    # Displays a list of all registered users (requires authentication)
    model = User
    context_object_name = "users"
    template_name = "security/user_list.html"  # Ensure this template exists


class ViewUserDetails(LoginRequiredMixin, DetailView):
    # Displays details of a specific user (requires authentication)
    model = User
    context_object_name = "user"
    template_name = "security/user_detail.html"  # Ensure this template exists


class CreateNewUser(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    # Allows HR Admins to create a new user
    model = User
    form_class = UserForm
    template_name = "security/user_form.html"
    success_url = reverse_lazy("security:user_list")

    def test_func(self):
        return self.request.user.groups.filter(name="HR Admin").exists()


class UpdateUser(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # Allows HR Admins to update user details
    model = User
    form_class = UserForm
    template_name = "security/user_form.html"
    success_url = reverse_lazy("security:user_list")

    def test_func(self):
        return self.request.user.groups.filter(name="HR Admin").exists()


class DeleteUser(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    # Allows HR Admins to delete a user
    model = User
    template_name = "security/user_confirm_delete.html"
    success_url = reverse_lazy("security:user_list")

    def test_func(self):
        return self.request.user.groups.filter(name="HR Admin").exists()
    

class GroupForm(forms.ModelForm):
    # Form for creating and editing Django's built-in groups
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']


@permission_required('auth.view_group', raise_exception=True)
def group_list(request):
    # Displays a list of all groups (requires view_group permission)
    groups = Group.objects.all()
    return render(request, 'security/group_list.html', {'groups': groups})


@permission_required('auth.change_group', raise_exception=True)
def group_edit(request, pk=None):
    # Creates or edits a group (requires change_group permission)
    group = get_object_or_404(Group, pk=pk) if pk else None

    if request.method == "POST":
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('security:group_list')
    else:
        form = GroupForm(instance=group)

    return render(request, 'security/group_form.html', {'form': form, 'group': group})


@permission_required('auth.delete_group', raise_exception=True)
def group_delete(request, pk):
    # Deletes a group after confirmation (requires delete_group permission)
    group = get_object_or_404(Group, pk=pk)

    if request.method == "POST":
        group.delete()
        return redirect('security:group_list')

    return render(request, 'security/group_confirm_delete.html', {'group': group})
