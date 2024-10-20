from django.shortcuts import render
from people_management.models import Person

# Create your views here.
def dashboard(request):
    people = Person.objects.all()
    return render(request, 'dashboard/dashboard.html', {'people': people})

def test(request):
    return render(request, "dashboard/test.html")
    