from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from security.models import Role, PermissionDefinition
from people_management.models import Person
from datetime import date


class RolePermissionTests(TestCase):
    """Test case for role-based permissions system."""

    def setUp(self):
        """Set up initial test data for roles, permissions, and users."""
        # Create permission objects
        self.view_person = PermissionDefinition.objects.create(
            codename="view_person", 
            name="View Person", 
            description="Allows viewing of employee records"
        )
        self.change_person = PermissionDefinition.objects.create(
            codename="change_person", 
            name="Change Person", 
            description="Allows editing of employee records"
        )

        # Create predefined roles
        self.employee_role = Role.objects.create(name="Employee", description="Basic Employee Role")
        self.manager_role = Role.objects.create(name="Manager", description="Manager Role")

        # Assign permissions to roles
        self.employee_role.permissions.add(self.view_person)  # Employees can only view
        self.manager_role.permissions.add(self.view_person, self.change_person)  # Managers can view & edit

        # Create a user and link them to the Employee role
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.person = Person.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            date_of_birth=date(1990, 1, 1), 
            role=self.employee_role,
            user=self.user
        )
        
    def test_role_permissions_assignment(self):
        """Test that roles have the correct permissions assigned."""
        self.assertIn(self.view_person, self.employee_role.permissions.all())  # Employee has view permission
        self.assertIn(self.view_person, self.manager_role.permissions.all())  # Manager has view permission
        self.assertIn(self.change_person, self.manager_role.permissions.all())  # Manager has edit permission
        self.assertNotIn(self.change_person, self.employee_role.permissions.all())  # Employee should not have edit permission

    def test_user_inherits_permissions_from_role(self):
        """Test that a user correctly inherits permissions from their assigned role."""
        self.assertTrue(self.user.has_perm("view_person"))  # Employee should have this
        self.assertFalse(self.user.has_perm("change_person"))  # Employee shouldn't have this

        # Change user's role to Manager and check new permissions
        self.person.role = self.manager_role
        self.person.save()

        self.assertTrue(self.user.has_perm("view_person"))  # Manager should still have view permission
        self.assertTrue(self.user.has_perm("change_person"))  # Manager should now have edit permission

    def test_predefined_roles_cannot_be_renamed(self):
        """Ensure predefined roles cannot be renamed."""
        with self.assertRaises(ValidationError):
            self.employee_role.name = "Super Employee"
            self.employee_role.clean()  # Should raise ValidationError due to role restrictions

    def test_predefined_roles_cannot_be_deleted(self):
        """Ensure predefined roles cannot be deleted."""
        with self.assertRaises(ValidationError):
            self.employee_role.delete()  # Should raise ValidationError

    def test_custom_roles_can_be_created_and_deleted(self):
        """Ensure that custom roles can be added and deleted successfully."""
        custom_role = Role.objects.create(name="Supervisor", description="Custom role")
        self.assertEqual(Role.objects.filter(name="Supervisor").count(), 1)  # Role should exist

        custom_role.delete()
        self.assertEqual(Role.objects.filter(name="Supervisor").count(), 0)  # Role should be deleted

    def test_permissions_can_be_added_and_removed(self):
        """Ensure permissions can be dynamically assigned to and removed from roles."""
        self.manager_role.permissions.remove(self.change_person)  # Remove edit permission from Manager
        self.assertNotIn(self.change_person, self.manager_role.permissions.all())

        self.manager_role.permissions.add(self.change_person)  # Re-add edit permission
        self.assertIn(self.change_person, self.manager_role.permissions.all())

    def test_user_does_not_have_direct_permissions(self):
        """Ensure users only get permissions from their assigned role, not from direct assignments."""
        self.user.user_permissions.add(self.change_person)  # Try to assign edit permission directly
        self.assertFalse(self.user.has_perm("change_person"))  # Should still be False

    def test_assigning_role_to_user_updates_permissions(self):
        """Test that assigning a new role to a user updates their permissions correctly."""
        self.person.role = self.manager_role  # Assign Manager role to user
        self.person.save()

        self.assertTrue(self.user.has_perm("view_person"))  # Manager should have view permission
        self.assertTrue(self.user.has_perm("change_person"))  # Manager should have edit permission

    def test_removing_role_removes_permissions(self):
        """Ensure removing a user's role revokes their permissions."""
        self.person.role = None  # Remove role from user
        self.person.save()

        self.assertFalse(self.user.has_perm("view_person"))  # Should no longer have view permission
        self.assertFalse(self.user.has_perm("change_person"))  # Should no longer have edit permission
