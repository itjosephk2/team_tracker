from django.test import TestCase
from django.contrib.auth.models import User, Group, Permission
from django.urls import reverse
from security.forms import CustomUserCreationForm, CustomUserUpdateForm, GroupForm
from people_management.models import Person


class CustomUserCreationFormTests(TestCase):
    def setUp(self):
        self.person = Person.objects.create(
            first_name="Test",
            last_name="User",
            email="testuser@example.com",
            date_of_birth="1990-01-01",
            role="employee"
        )

    def test_valid_form_creates_user(self):
        form_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "person": self.person.id,
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_duplicate_username_fails(self):
        User.objects.create(username="takenuser")
        form_data = {
            "username": "takenuser",
            "email": "someone@example.com",
            "person": self.person.id,
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)


class CustomUserUpdateFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="updatable", email="old@example.com")

    def test_update_email(self):
        form = CustomUserUpdateForm(
            instance=self.user,
            data={"username": "updatable", "email": "new@example.com"}
        )
        self.assertTrue(form.is_valid())
        updated_user = form.save()
        self.assertEqual(updated_user.email, "new@example.com")


class GroupFormTests(TestCase):
    def test_group_creation_with_permissions(self):
        permission = Permission.objects.first()
        form = GroupForm(data={"name": "HR Group", "permissions": [permission.id]})
        self.assertTrue(form.is_valid())
        group = form.save()
        self.assertIn(permission, group.permissions.all())


class UserViewTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="adminpass", is_staff=True)
        permission = Permission.objects.get(codename="view_user")
        self.admin.user_permissions.add(permission)

    def test_user_list_view_requires_login(self):
        response = self.client.get(reverse("security:user_list"))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_user_list_view_as_logged_in_user(self):
        self.client.login(username="admin", password="adminpass")
        response = self.client.get(reverse("security:user_list"))
        self.assertEqual(response.status_code, 200)
