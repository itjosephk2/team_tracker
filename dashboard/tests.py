from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from dashboard.forms import CustomUserCreationForm, CustomLoginForm
from people_management.models import Person
from security.models import Role
from datetime import date


class CustomUserCreationFormTest(TestCase):
    def test_valid_user_creation(self):
        form_data = {
            "username": "testuser",
            "password1": "TestPassword123!",
            "password2": "TestPassword123!",
            "is_staff": True
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

        user = form.save()
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.is_staff)  # Ensure staff status is correctly assigned

    def test_invalid_user_creation(self):
        form_data = {
            "username": "",
            "password1": "password",
            "password2": "password"
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())  # Form should be invalid due to missing username


class CustomLoginFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="TestPassword123!")

    def test_valid_login(self):
        form_data = {
            "username": "testuser",
            "password": "TestPassword123!"
        }
        form = CustomLoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_login(self):
        form_data = {
            "username": "wronguser",
            "password": "wrongpassword"
        }
        form = CustomLoginForm(data=form_data)
        self.assertFalse(form.is_valid())  # Invalid credentials should fail validation


class DashboardViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="TestPassword123!")
        self.role = Role.objects.create(name="Employee")
        self.person = Person.objects.create(
            first_name="Alice",
            last_name="Smith",
            email="alice.smith@example.com",
            date_of_birth=date(2024, 1, 1),
            role=self.role,
            user=self.user
        )

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_dashboard_accessible_for_logged_in_user(self):
        self.client.login(username="testuser", password="TestPassword123!")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alice")  # Ensuring person data is loaded in context
