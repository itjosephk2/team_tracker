"""
Tests for the people_management app.

This module includes tests for the PersonForm and ContractForm validations,
as well as tests for model behaviors (including updating active status via
the update_active_status method and signal-triggered status updates).
"""

from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase

from .forms import PersonForm, ContractForm
from .models import Person, Contract


class PersonFormTestCase(TestCase):
    """
    Test cases for the PersonForm.
    """

    def setUp(self):
        """
        Set up test data with a manager and an employee.
        """
        self.manager = Person.objects.create(
            first_name="Manager",
            last_name="Test",
            email="manager@example.com",
            phone_number="1234567890",
            date_of_birth=date(1980, 1, 1),
            role="manager",
            active=True
        )
        self.employee = Person.objects.create(
            first_name="Employee",
            last_name="Test",
            email="employee@example.com",
            phone_number="1234567890",
            date_of_birth=date(1990, 1, 1),
            role="employee",
            active=True
        )

    def test_invalid_email(self):
        """
        Test that the form raises an error when the email lacks an '@' symbol.
        """
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoeexample.com',  # Invalid email (missing '@')
            'phone_number': '1234567890',
            'date_of_birth': '1990-01-01',
            'role': 'employee',
            'manager': self.manager.id,
        }
        form = PersonForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_empty_first_name(self):
        """
        Test that the form raises an error when the first name is empty.
        """
        form_data = {
            'first_name': '   ',  # Whitespace only should be invalid
            'last_name': 'Doe',
            'email': 'john@doe.com',
            'phone_number': '1234567890',
            'date_of_birth': '1990-01-01',
            'role': 'employee',
            'manager': self.manager.id,
        }
        form = PersonForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)

    def test_underage_date_of_birth(self):
        """
        Test that the form raises an error if the person is under 16 years old.
        """
        underage_date = date.today() - timedelta(days=15 * 365)  # Approximate 15 years old
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@doe.com',
            'phone_number': '1234567890',
            'date_of_birth': underage_date,
            'role': 'employee',
            'manager': self.manager.id,
        }
        form = PersonForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('date_of_birth', form.errors)

    def test_invalid_manager(self):
        """
        Test that the form raises an error if an employee (not a manager) is selected as manager.
        """
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@doe.com',
            'phone_number': '1234567890',
            'date_of_birth': '1990-01-01',
            'role': 'employee',
            'manager': self.employee.id,  # Employee cannot be a manager
        }
        form = PersonForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('manager', form.errors)

    def test_valid_person_form(self):
        """
        Test that the form is valid when provided with proper data.
        """
        form_data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane@doe.com',
            'phone_number': '1234567890',
            'date_of_birth': '1990-01-01',
            'role': 'employee',
            'manager': self.manager.id,
        }
        form = PersonForm(data=form_data)
        self.assertTrue(form.is_valid())


class ContractFormTestCase(TestCase):
    """
    Test cases for the ContractForm.
    """

    def setUp(self):
        """
        Set up test data with a Person instance.
        """
        self.person = Person.objects.create(
            first_name="John",
            last_name="Smith",
            email="johnsmith@example.com",
            phone_number="1234567890",
            date_of_birth=date(1990, 1, 1),
            role="employee",
            active=True
        )

    def test_invalid_hourly_rate(self):
        """
        Test that the form raises an error if the hourly rate is below 12.45.
        """
        form_data = {
            'person': self.person.id,
            'job_title': 'Developer',
            'contract_start': '2020-01-01',
            'contract_end': '2022-01-01',
            'hourly_rate': 10,  # Invalid: below minimum threshold
            'contracted_hours': 40,
        }
        form = ContractForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('hourly_rate', form.errors)

    def test_invalid_contract_end_date(self):
        """
        Test that the form raises an error when the contract end date is before the start date.
        """
        form_data = {
            'person': self.person.id,
            'job_title': 'Developer',
            'contract_start': '2022-01-01',
            'contract_end': '2021-12-31',  # End date before start date
            'hourly_rate': 15,
            'contracted_hours': 40,
        }
        form = ContractForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('contract_end', form.errors)

    def test_valid_contract_form(self):
        """
        Test that the contract form is valid with correct data.
        """
        form_data = {
            'person': self.person.id,
            'job_title': 'Developer',
            'contract_start': '2020-01-01',
            'contract_end': '2022-01-01',
            'hourly_rate': 15,
            'contracted_hours': 40,
        }
        form = ContractForm(data=form_data)
        self.assertTrue(form.is_valid())


class ModelTestCase(TestCase):
    """
    Test cases for the Person and Contract model behaviors, including signals.
    """

    def setUp(self):
        """
        Set up a Person instance for testing model methods and signal behavior.
        """
        self.person = Person.objects.create(
            first_name="Alice",
            last_name="Wonder",
            email="alice@example.com",
            phone_number="1234567890",
            date_of_birth=date(1985, 1, 1),
            role="employee",
            active=False
        )

    def test_update_active_status(self):
        """
        Test that the update_active_status method activates a person if a valid contract exists.
        """
        today = date.today()
        Contract.objects.create(
            person=self.person,
            job_title="Tester",
            contract_start=today - timedelta(days=1),
            contract_end=today + timedelta(days=10),
            hourly_rate=15,
            contracted_hours=40,
        )
        # Update active status based on current contracts
        self.person.update_active_status()
        self.assertTrue(self.person.active)

    def test_activate_person_on_contract_save(self):
        """
        Test that saving a valid contract triggers the signal to activate the person.
        """
        today = date.today()
        # Ensure the person is inactive
        self.person.active = False
        self.person.save()

        Contract.objects.create(
            person=self.person,
            job_title="Tester",
            contract_start=today - timedelta(days=5),
            contract_end=today + timedelta(days=5),
            hourly_rate=15,
            contracted_hours=40,
        )
        # Refresh person from the database to reflect any signal-triggered changes
        self.person.refresh_from_db()
        self.assertTrue(self.person.active)

    def test_deactivate_person_on_contract_delete(self):
        """
        Test that deleting a contract triggers the signal to deactivate the person if no valid contracts remain.
        """
        today = date.today()
        contract = Contract.objects.create(
            person=self.person,
            job_title="Tester",
            contract_start=today - timedelta(days=10),
            contract_end=today + timedelta(days=10),
            hourly_rate=15,
            contracted_hours=40,
        )
        # Ensure person becomes active after contract is saved
        self.person.update_active_status()
        self.assertTrue(self.person.active)

        # Delete the contract and verify the person is deactivated
        contract.delete()
        self.person.refresh_from_db()
        self.assertFalse(self.person.active)
