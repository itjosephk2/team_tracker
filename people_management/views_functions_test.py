from django.shortcuts import render, get_object_or_404
from people_management.models import Person


def person_details_view(request, pk):
    person = get_object_or_404(Person, pk=pk)  # ✅ Fetch specific person
    return render(request, 'people_management/person_detail.html', {'person': person})  