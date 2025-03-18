import django_filters
from django import forms
from .models import Contract
from people_management.models import Person

class ContractFilter(django_filters.FilterSet):
    person = django_filters.ModelChoiceFilter(
        queryset=Person.objects.all(),
        label='Person',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Contract
        fields = ['person']