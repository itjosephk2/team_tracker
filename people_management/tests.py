from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from dashboard.forms import CustomUserCreationForm, CustomLoginForm
from people_management.models import Person
from datetime import date


class CustomUserCreationFormTest(TestCase):
    """
    Test cases for the CustomUserCreationForm.
    Ensures user creation behaves correctly.
    """
    
    def test_valid_user_creation(self):
        """Test that a valid user creation form results in a new user being created."""
        form_data = {
            "username": "testuser",
            "password1": "TestPassword123!",
            "password2": "TestPassword123!",
            "is_staff": True
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())  # Form should be valid

        user = form.save()
        self.assertEqual(user.username, "testuser")  # Ensure correct username
        self.assertTrue(user.is_staff)  # Ensure staff status is correctly assigned

    def test_invalid_user_creation(self):
        """Test that an invalid user creation form fails validation."""
        form_data = {
            "username": "",  # Missing username
            "password1": "password",
            "password2": "password"
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())  # Form should be invalid due to missing username


class CustomLoginFormTest(TestCase):
    """
    Test cases for the CustomLoginForm.
    Ensures login form validation works correctly.
    """
    
    def setUp(self):
        """Set up a test user for login validation."""
        self.user = User.objects.create_user(username="testuser", password="TestPassword123!")

    def test_valid_login(self):
        """Test that a valid login form allows authentication."""
        form_data = {
            "username": "testuser",
            "password": "TestPassword123!"
        }
        form = CustomLoginForm(data=form_data)
        self.assertTrue(form.is_valid())  # Form should be valid

    def test_invalid_login(self):
        """Test that an invalid login form fails validation."""
        form_data = {
            "username": "wronguser",
            "password": "wrongpassword"
        }
        form = CustomLoginForm(data=form_data)
        self.assertFalse(form.is_valid())  # Invalid credentials should fail validation


class DashboardViewTest(TestCase):
    """
    Test cases for the Dashboard view.
    Ensures that authentication and data rendering work correctly.
    """
    
    def setUp(self):
        """Set up a test user and associated Person record for dashboard access testing."""
        self.user = User.objects.create_user(username="testuser", password="TestPassword123!")
        self.person = Person.objects.create(
            first_name="Alice",
            last_name="Smith",
            email="alice.smith@example.com",
            date_of_birth=date(2024, 1, 1),
            user=self.user
        )

    def test_dashboard_requires_login(self):
        """Ensure unauthenticated users are redirected to the login page when accessing the dashboard."""
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)  # Expect redirect to login page

    def test_dashboard_accessible_for_logged_in_user(self):
        """Ensure logged-in users can access the dashboard and see relevant content."""
        self.client.login(username="testuser", password="TestPassword123!")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)  # Expect success response
        self.assertContains(response, "Alice")  # Ensure user's name appears in the respons