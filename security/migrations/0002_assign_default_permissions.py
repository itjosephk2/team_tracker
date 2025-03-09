from django.db import migrations


def create_permissions_and_assign_roles(apps, schema_editor):
    """Create system permissions and assign them to the default roles."""
    Role = apps.get_model("security", "Role")
    PermissionDefinition = apps.get_model("security", "PermissionDefinition")

    # Define default permissions
    permissions = [
        {"codename": "view_person", "name": "View Person", "description": "Allows viewing of employee records"},
        {"codename": "change_person", "name": "Change Person", "description": "Allows editing of employee records"},
        {"codename": "delete_person", "name": "Delete Person", "description": "Allows deleting of employee records"},
        {"codename": "add_person", "name": "Add Person", "description": "Allows adding new employees"},
        {"codename": "view_contract", "name": "View Contract", "description": "Allows viewing of contracts"},
        {"codename": "change_contract", "name": "Change Contract", "description": "Allows editing of contracts"},
        {"codename": "delete_contract", "name": "Delete Contract", "description": "Allows deleting of contracts"},
        {"codename": "add_contract", "name": "Add Contract", "description": "Allows adding new contracts"},
    ]

    # Fetch or create the predefined roles
    employee_role, _ = Role.objects.get_or_create(name="Employee")
    manager_role, _ = Role.objects.get_or_create(name="Manager")
    hr_admin_role, _ = Role.objects.get_or_create(name="HR Admin")

    # Create permissions and assign them to roles
    for perm in permissions:
        permission, _ = PermissionDefinition.objects.get_or_create(
            codename=perm["codename"],
            defaults={"name": perm["name"], "description": perm["description"]}
        )

        # Assign permissions to roles
        if perm["codename"] in ["view_person", "view_contract"]:
            employee_role.permissions.add(permission)
            manager_role.permissions.add(permission)
            hr_admin_role.permissions.add(permission)

        if perm["codename"] in ["change_person", "change_contract"]:
            manager_role.permissions.add(permission)
            hr_admin_role.permissions.add(permission)

        if perm["codename"] in ["delete_person", "delete_contract", "add_person", "add_contract"]:
            hr_admin_role.permissions.add(permission)

    # Save role updates
    employee_role.save()
    manager_role.save()
    hr_admin_role.save()


class Migration(migrations.Migration):
    dependencies = [
        ("security", "0001_initial"),  # Ensure this references the correct initial migration
    ]

    operations = [
        migrations.RunPython(create_permissions_and_assign_roles),
    ]
