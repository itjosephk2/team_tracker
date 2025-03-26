from django.core.management.base import BaseCommand
from security.models import Role, PermissionDefinition


class Command(BaseCommand):
    help = "Populates the database with default roles and permissions"

    def handle(self, *args, **kwargs):
        # Define system-managed permissions (No references to employees or reports)
        permissions = {
            "view_dashboard": "Access the main dashboard.",
            "view_people_list": "See the list of people.",
            "view_settings": "Access the settings page.",
            "view_person": "View person details.",
            "change_person": "Edit person information.",
            "delete_person": "Remove a person from the system.",
            "add_person": "Add a new person to the system.",
        }

        # Create permissions
        for codename, name in permissions.items():
            perm, created = PermissionDefinition.objects.get_or_create(
                codename=codename, defaults={"name": name, "description": name}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created permission: {codename}"))

        # Define default roles with their associated permissions
        roles = {
            "Employee": ["view_dashboard", "view_people_list", "view_person"],
            "Manager": [
                "view_dashboard",
                "view_people_list",
                "view_person",
                "change_person",
            ],
            "HR Admin": [
                "view_dashboard",
                "view_people_list",
                "view_settings",
                "view_person",
                "change_person",
                "delete_person",
                "add_person",
            ],
        }

        # Create roles
        for role_name, perms in roles.items():
            role, created = Role.objects.get_or_create(
                name=role_name,
                defaults={
                    "description": f"System role: {role_name}",
                    "is_default": True,
                },
            )

            # Assign permissions
            for perm_codename in perms:
                perm = PermissionDefinition.objects.get(codename=perm_codename)
                role.permissions.add(perm)

            if created:
                self.stdout.write(self.style.SUCCESS(f"Created role: {role_name}"))

        self.stdout.write(
            self.style.SUCCESS("Default roles and permissions populated successfully!")
        )
