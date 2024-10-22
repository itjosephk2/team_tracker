from typing import List
from django.shortcuts import render
from django.http import Http404
from django.views.generic import ListView, DetailView, CreateView

from people_management.models import Person

# Create your views here.
class ListPeopleView(ListView):
    model = Person
    context_object_name = 'people'
    template_name = 'people_management/list_people.html'

class ViewPersonDetails(DetailView):
    model = Person
    context_object_name = 'person'
    template_name = 'people_management/view_person.html'

class AddNewPerson(CreateView):
    model = Person
    fields = ['first_name', 'last_name', 'email', ]
    template_name = 'people_management/create_person.html'
