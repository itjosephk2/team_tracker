# Generated by Django 4.2.16 on 2025-03-12 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("security", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="role",
            name="permissions",
        ),
        migrations.DeleteModel(
            name="PermissionDefinition",
        ),
        migrations.DeleteModel(
            name="Role",
        ),
    ]
