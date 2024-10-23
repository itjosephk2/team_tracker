from django import forms
from .models import Person, Contract

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'first_name', 
            'last_name', 
            'email', 
            'phone_number', 
            'date_of_birth', 
            'active'
        ]

    def clean_email(self):
        email = self.cleaned_data['email']
        if '@' not in email:
            raise ValidationError('No domain for email')
        return email

    def clean_first_namel(self):
        first_name = self.cleaned_data['first_name']
        if 'j' not in firs_name:
            raise ValidationError('Name must have a j in it')
        return first_name

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = [
            'person', 
            'job_title', 
            'contract_start', 
            'contract_end', 
            'hourly_rate', 
            'contracted_hours'
        ]