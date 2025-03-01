from typing import List
from django.shortcuts import render
from django.http import Http404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm  # Assuming you have these forms


# User Views
class ListUsers(ListView):
    model = User
    context_object_name = 'users'


class ViewUserDetails(DetailView):
    model = User
    context_object_name = 'user'


class CreateNewUser(CreateView):
    model = User
    form_class = CustomUserCreationForm  # Custom form for user creation
    success_url = reverse_lazy('users')  # Redirect to user list after successful creation


class UpdateUser(UpdateView):
    model = User
    form_class = CustomUserChangeForm  # Custom form for user updating
    success_url = reverse_lazy('users')  # Redirect to user list after successful update


class DeleteUser(DeleteView):
    model = User
    success_url = reverse_lazy('users')  # Redirect to user list after deletion
