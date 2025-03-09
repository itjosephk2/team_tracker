from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from people_management.models import Person, Contract
from security.models import Role, PermissionDefinition
from datetime import date


class PersonModelTest(TestCase):
    """Tests for the Person model."""

    def setUp(self):
        """Set up test data for Person model."""
        self.role = Role.objects.create(name="Employee")  # Create a role
        self.person = Person.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            date_of_birth=date(1990, 1, 1), 
            role=self.role
        )

    def test_person_creation(self):
        """Test that a Person object is created correctly."""
        self.assertEqual(self.person.first_name, "John")
        self.assertEqual(self.person.date_of_birth, date(1990, 1, 1))

        # Ensure predefined roles exist in the database
        self.employee_role, _ = Role.objects.get_or_create(
            name="Employee", defaults={"description": "Basic Employee Role"}
        )
        self.manager_role, _ = Role.objects.get_or_create(
            name="Manager", defaults={"description": "Manager Role"}
        )


class ContractModelTest(TestCase):
    """Tests for the Contract model."""

    def setUp(self):
        """Set up test data for Contract model."""
        # Create a role and assign it to a person
        self.role = Role.objects.create(name="Employee")
        self.person = Person.objects.create(
            first_name="Alice",
            last_name="Smith",
            email="alice.smith@example.com",
            date_of_birth=date(1990, 1, 1), 
            role=self.role,
        )

        # Create a contract for the person
        self.contract = Contract.objects.create(
            person=self.person,
            job_title="Software Engineer",
            contract_start=date(2024, 2, 15),
            hourly_rate=25.00,
            contracted_hours=40,
        )

    def test_contract_creation(self):
        """Test that a Contract object is created correctly."""
        self.assertEqual(self.contract.job_title, "Software Engineer")
        self.assertEqual(self.contract.person.first_name, "Alice")


class UserAuthenticationTest(TestCase):
    """Tests for user authentication."""

    def setUp(self):
        """Set up a test user."""
        self.user = User.objects.create_user(username="testuser", password="password")

    def test_login(self):
        """Test that a user can successfully log in."""
        login = self.client.login(username="testuser", password="password")
        self.assertTrue(login)


class RolePermissionsTest(TestCase):
    """Tests for assigning permissions to roles."""

    def setUp(self):
        """Set up a role and assign permissions."""
        self.permission = PermissionDefinition.objects.create(
            codename="view_person", name="View Person"
        )
        self.role = Role.objects.create(name="Manager")
        self.role.permissions.add(self.permission)  # Assign permission to role

    def test_role_permission_assignment(self):
        """Test that a role has the correct assigned permissions."""
        self.assertTrue(self.role.permissions.filter(codename="view_person").exists())


class PersonListViewTest(TestCase):
    """Tests for the person list view."""

    def setUp(self):
        """Set up a test user and log in."""
        self.user = User.objects.create_user(username="admin", password="password")
        self.client.login(username="admin", password="password")

    def test_person_list_view(self):
        """Test that the person list view is accessible."""
        response = self.client.get(reverse("people"))  # Ensure URL name matches views.py
        self.assertEqual(response.status_code, 200)
