from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType


class UserManagementTests(TestCase):
    """Tests for user management views."""

    def setUp(self):
        # Create HR Admin group with necessary permissions
        self.hr_admin_group = Group.objects.create(name="HR Admin")
        self.hr_admin_user = User.objects.create_user(username="hradmin", password="password")
        self.hr_admin_user.groups.add(self.hr_admin_group)

        # Create a regular user
        self.regular_user = User.objects.create_user(username="user", password="password")

        # Client for testing
        self.client.login(username="hradmin", password="password")

    def test_list_users_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("security:user_list"))
        self.assertRedirects(response, f"/accounts/login/?next={reverse('security:user_list')}")

    def test_list_users_successful(self):
        response = self.client.get(reverse("security:user_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "security/user_list.html")

    def test_view_user_details_successful(self):
        response = self.client.get(reverse("security:user_detail", args=[self.regular_user.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "security/user_detail.html")

    def test_create_user_requires_hr_admin(self):
        response = self.client.post(reverse("security:user_add"), {
            "username": "newuser",
            "password": "testpassword",
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after creation
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_update_user_requires_hr_admin(self):
        response = self.client.post(reverse("security:user_edit", args=[self.regular_user.pk]), {
            "username": "updateduser",
        })
        self.assertEqual(response.status_code, 302)
        self.regular_user.refresh_from_db()
        self.assertEqual(self.regular_user.username, "updateduser")

    def test_delete_user_requires_hr_admin(self):
        response = self.client.post(reverse("security:user_delete", args=[self.regular_user.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(pk=self.regular_user.pk).exists())


class GroupManagementTests(TestCase):
    """Tests for group management views."""

    def setUp(self):
        # Create an HR Admin with permission to manage groups
        self.hr_admin_user = User.objects.create_user(username="hradmin", password="password")
        self.group_manage_permission = Permission.objects.create(
            codename="manage_groups",
            name="Can manage groups",
            content_type=ContentType.objects.get_for_model(Group),
        )
        self.hr_admin_user.user_permissions.add(self.group_manage_permission)
        self.client.login(username="hradmin", password="password")

        # Create a test group
        self.test_group = Group.objects.create(name="Test Group")

    def test_list_groups_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("security:group_list"))
        self.assertRedirects(response, f"/accounts/login/?next={reverse('security:group_list')}")

    def test_list_groups_successful(self):
        response = self.client.get(reverse("security:group_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "security/group_list.html")

    def test_create_group_successful(self):
        response = self.client.post(reverse("security:group_add"), {
            "name": "New Group",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Group.objects.filter(name="New Group").exists())

    def test_edit_group_successful(self):
        response = self.client.post(reverse("security:group_edit", args=[self.test_group.pk]), {
            "name": "Updated Group",
        })
        self.assertEqual(response.status_code, 302)
        self.test_group.refresh_from_db()
        self.assertEqual(self.test_group.name, "Updated Group")

    def test_delete_group_successful(self):
        response = self.client.post(reverse("security:group_delete", args=[self.test_group.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Group.objects.filter(pk=self.test_group.pk).exists())
