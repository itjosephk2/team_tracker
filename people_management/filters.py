import django_filters
from .models import Contract
from people_management.models import Person


class ContractFilter(django_filters.FilterSet):
    job_title = django_filters.CharFilter(field_name='job_title', lookup_expr='icontains', label='Job Title')
    person = django_filters.ModelChoiceFilter(queryset=Person.objects.all(), label='Person')

    class Meta:
        model = Contract
        fields = ['job_title', 'person']
