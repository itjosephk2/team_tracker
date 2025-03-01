from django.shortcuts import render
from django.http import Http404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User  # Import User model for authentication
# from .forms import UserForm  # Ensure UserForm is properly defined


# User Views
class ListUser(ListView):
    model = User
    context_object_name = 'users'  # Display all users
    template_name = 'security/list_users.html'  # Optional: Add custom template for listing users


class ViewUserDetails(DetailView):
    model = User
    context_object_name = 'user'  # Display details of a specific user
    template_name = 'security/view_user_details.html'


class CreateNewUser(CreateView):
    model = User
    # form_class = UserForm  # Assuming UserForm is used for creating new users
    success_url = reverse_lazy('users')  # Redirect to user list after creation
    template_name = 'security/create_user.html'  # Optional: Add custom template for creating users


class UpdateUser(UpdateView):
    model = User
    # form_class = UserForm  # Assuming UserForm is used for updating users
    success_url = reverse_lazy('users')  # Redirect to user list after update
    template_name = 'security/update_user.html'  # Optional: Add custom template for updating users


class DeleteUser(DeleteView):
    model = User
    success_url = reverse_lazy('users')  # Redirect to user list after deletion
    template_name = 'security/confirm_delete.html'  # Optional: Confirm delete template
