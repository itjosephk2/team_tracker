from django.shortcuts import render
from people_management.models import Person

# Create your views here.
def list_people(request):
    people = Person.objects.all()
    return render(request, 'people_management/list_people.html', {'people': people})

def view_person(request, pk):
    person = Person.objects.get(pk=pk)
    return render(request, 'people_management/view_person.html', {'person' : person})

# def add(request):
#     people = Person.objects.all()
#     return render(request, 'people_management/create_person.html', {'people': people})