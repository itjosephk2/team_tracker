from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from dashboard.forms import CustomUserCreationForm, CustomLoginForm
from people_management.models import Person
from datetime import date


class CustomUserCreationFormTest(TestCase):
    """
    Unit tests for the CustomUserCreationForm.
    Verifies that the user registration form validates input correctly and saves users as expected.
    """

    def test_valid_user_creation(self):
        """
        Test that a valid form submission successfully creates a user
        with the correct username and staff status.
        """
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
        self.assertTrue(user.is_staff)

    def test_invalid_user_creation(self):
        """
        Test that form submission fails when required fields (e.g., username)
        are missing or invalid.
        """
        form_data = {
            "username": "",
            "password1": "password",
            "password2": "password"
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())


class CustomLoginFormTest(TestCase):
    """
    Unit tests for the CustomLoginForm.
    Ensures correct validation behavior for both valid and invalid login attempts.
    """

    def setUp(self):
        """
        Create a test user for login form validation tests.
        """
        self.user = User.objects.create_user(username="testuser", password="TestPassword123!")

    def test_valid_login(self):
        """
        Test that the form is valid when correct credentials are entered.
        """
        form_data = {
            "username": "testuser",
            "password": "TestPassword123!"
        }
        form = CustomLoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_login(self):
        """
        Test that the form fails validation with incorrect credentials.
        """
        form_data = {
            "username": "wronguser",
            "password": "wrongpassword"
        }
        form = CustomLoginForm(data=form_data)
        self.assertFalse(form.is_valid())


class DashboardViewTest(TestCase):
    """
    Integration tests for the dashboard view.
    Confirms access control and content rendering based on authentication status and user role.
    """

    def setUp(self):
        """
        Set up a test user and corresponding Person record.
        """
        self.user = User.objects.create_user(username="testuser", password="TestPassword123!")
        self.person = Person.objects.create(
            first_name="Alice",
            last_name="Smith",
            email="alice.smith@example.com",
            date_of_birth=date(2024, 1, 1),
            user=self.user
        )

    def test_dashboard_requires_login(self):
        """
        Ensure unauthenticated users are redirected to the login page.
        """
        response = self.client.get(reverse("dashboard:dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_accessible_for_logged_in_user(self):
        """
        Ensure authenticated users can access the dashboard and see personalized content.
        """
        self.client.login(username="testuser", password="TestPassword123!")
        response = self.client.get(reverse("dashboard:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alice")
