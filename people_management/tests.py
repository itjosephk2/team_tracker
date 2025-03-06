from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from people_management.models import Person, Contract
from security.models import Role, PermissionDefinition
from datetime import date


class PersonModelTest(TestCase):
    def setUp(self):
        self.role = Role.objects.create(name="Employee")
        self.person = Person.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            date_of_birth=date(1990, 1, 1), 
            role=self.role
        )

    def test_person_creation(self):
        self.assertEqual(self.person.first_name, "John")
        self.assertEqual(self.person.role.name, "Employee")
        self.assertEqual(self.person.date_of_birth, date(1990, 1, 1)) 


class ContractModelTest(TestCase):
    def setUp(self):
        self.role = Role.objects.create(name="Employee")
        self.person = Person.objects.create(
            first_name="Alice",
            last_name="Smith",
            email="alice.smith@example.com",
            date_of_birth=date(1990, 1, 1), 
            role=self.role,
        )
        self.contract = Contract.objects.create(
            person=self.person,
            job_title="Software Engineer",
            contract_start=date(2024, 2, 15),
            hourly_rate=25.00,
            contracted_hours=(40),
        )

    def test_contract_creation(self):
        self.assertEqual(self.contract.job_title, "Software Engineer")
        self.assertEqual(self.contract.person.first_name, "Alice")


class UserAuthenticationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")

    def test_login(self):
        login = self.client.login(username="testuser", password="password")
        self.assertTrue(login)


class RolePermissionsTest(TestCase):
    def setUp(self):
        self.permission = PermissionDefinition.objects.create(codename="view_person", name="View Person")
        self.role = Role.objects.create(name="Manager")
        self.role.permissions.add(self.permission)

    def test_role_permission_assignment(self):
        self.assertTrue(self.role.permissions.filter(codename="view_person").exists())


class PersonListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="admin", password="password")
        self.client.login(username="admin", password="password")

    def test_person_list_view(self):
        response = self.client.get(reverse("people"))
        self.assertEqual(response.status_code, 200)