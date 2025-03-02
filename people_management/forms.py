from django import forms
from django.core.exceptions import ValidationError
from datetime import date
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
            'role',  # New field for the person's role
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'role': forms.Select(attrs={'class': 'form-select'}),  # Widget for role selection
        }
        error_messages = {
            'first_name': {'max_length': 'First name cannot be longer than 50 characters!'},
            'last_name': {'max_length': 'Last name cannot be longer than 50 characters!'},
            'email': {'max_length': 'Email cannot be longer than 255 characters!'},
            'phone_number': {'max_length': 'Phone number cannot be longer than 15 characters!'},
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if '@' not in email:
            raise ValidationError('No domain for email')
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', '').strip()
        if not first_name:
            raise ValidationError('First name cannot be empty')
        return first_name

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if dob:
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 16:
                raise ValidationError('Person must be at least 16 years old')
        return dob


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
        widgets = {
            'person': forms.Select(attrs={'class': 'form-select'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title'}),
            'contract_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'contract_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hourly_rate': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Hourly Rate'}),
            'contracted_hours': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Contracted Hours'}),
        }
        error_messages = {
            'job_title': {'max_length': 'Job title cannot be longer than 255 characters!'},
        }

    def clean_hourly_rate(self):
        hourly_rate = self.cleaned_data.get('hourly_rate')
        if hourly_rate is not None and hourly_rate < 12.45:
            raise ValidationError('Hourly rate cannot be lower than 12.45')
        return hourly_rate

    def clean_contract_end(self):
        contract_start = self.cleaned_data.get('contract_start')
        contract_end = self.cleaned_data.get('contract_end')
        
        if contract_end and contract_start and contract_end <= contract_start:
            raise ValidationError('Contract end date must be after contract start date')
        
        return contract_end
