"""
This module defines Django forms for managing Person and Contract models.
It provides validation logic and custom widgets for each form field.
"""

from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from .models import Person, Contract


class PersonForm(forms.ModelForm):
    """
    Form for creating and updating Person instances.
    """

    class Meta:
        model = Person
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "date_of_birth",
            "role",
            "manager",
        ]
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "First Name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Last Name"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email"}
            ),
            "phone_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Phone Number"}
            ),
            "date_of_birth": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "role": forms.Select(attrs={"class": "form-select"}),
            "manager": forms.Select(attrs={"class": "form-select"}),
        }
        error_messages = {
            "first_name": {
                "max_length": "First name cannot be longer than 50 characters!"
            },
            "last_name": {
                "max_length": "Last name cannot be longer than 50 characters!"
            },
            "email": {"max_length": "Email cannot be longer than 255 characters!"},
            "phone_number": {
                "max_length": "Phone number cannot be longer than 15 characters!"
            },
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the PersonForm.

        Ensures the 'role' field is required and filters the 'manager' queryset
        to include only persons with roles 'manager' or 'hr_admin'.
        The 'manager' field remains optional.
        """
        super().__init__(*args, **kwargs)
        self.fields["role"].required = True
        self.fields["manager"].queryset = Person.objects.filter(
            role__in=["manager", "hr_admin"]
        )
        self.fields["manager"].required = False

    def clean_email(self):
        """
        Validate the email field to ensure it contains an '@' symbol.

        Raises:
            ValidationError: If the email does not contain an '@' symbol.
        """
        email = self.cleaned_data["email"]
        if "@" not in email:
            raise ValidationError("No domain for email")
        return email

    def clean_first_name(self):
        """
        Validate the first name field ensuring it is not empty after trimming.

        Raises:
            ValidationError: If the first name is empty.
        """
        first_name = self.cleaned_data.get("first_name", "").strip()
        if not first_name:
            raise ValidationError("First name cannot be empty")
        return first_name

    def clean_date_of_birth(self):
        """
        Validate the date of birth to ensure the person is at least 16 years old.

        Raises:
            ValidationError: If the person is younger than 16.
        """
        dob = self.cleaned_data.get("date_of_birth")
        if dob:
            today = date.today()
            age = (
                today.year
                - dob.year
                - ((today.month, today.day) < (dob.month, dob.day))
            )
            if age < 16:
                raise ValidationError("Person must be at least 16 years old")
        return dob

    def clean_manager(self):
        """
        Validate the manager field to ensure that an employee is not assigned as a manager.

        Raises:
            ValidationError: If the selected manager has the role 'employee'.
        """
        manager = self.cleaned_data.get("manager")
        if manager and manager.role == "employee":
            raise ValidationError("An employee cannot be assigned as a manager.")
        return manager


class ContractForm(forms.ModelForm):
    """
    Form for creating and updating Contract instances.
    """

    class Meta:
        model = Contract
        fields = [
            "person",
            "job_title",
            "contract_start",
            "contract_end",
            "hourly_rate",
            "contracted_hours",
        ]
        widgets = {
            "person": forms.Select(attrs={"class": "form-select"}),
            "job_title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Job Title"}
            ),
            "contract_start": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "contract_end": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "hourly_rate": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Hourly Rate"}
            ),
            "contracted_hours": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Contracted Hours"}
            ),
        }
        error_messages = {
            "job_title": {
                "max_length": "Job title cannot be longer than 255 characters!"
            },
        }

    def clean_hourly_rate(self):
        """
        Validate the hourly rate to ensure it meets the minimum threshold.

        Raises:
            ValidationError: If the hourly rate is below 12.45.
        """
        hourly_rate = self.cleaned_data.get("hourly_rate")
        if hourly_rate is not None and hourly_rate < 12.45:
            raise ValidationError("Hourly rate cannot be lower than 12.45")
        return hourly_rate

    def clean_contract_end(self):
        """
        Validate the contract end date to ensure it is after the contract start date.

        Raises:
            ValidationError: If the contract end date is not after the contract start date.
        """
        contract_start = self.cleaned_data.get("contract_start")
        contract_end = self.cleaned_data.get("contract_end")
        if contract_end and contract_start and contract_end <= contract_start:
            raise ValidationError("Contract end date must be after contract start date")
        return contract_end
