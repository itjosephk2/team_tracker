from django.shortcuts import render
from people_management.models import Person

# Create your views here.
def add(request):
    people = Person.objects.all()
    return render(request, 'people_management/create_person.html', {'people': people})

