from django.db import models
from django.contrib.auth.models import Permission


class PermissionDefinition(models.Model):
    """System-managed permissions with editable display names."""
    codename = models.CharField(max_length=100, unique=True)  # System identifier (fixed)
    name = models.CharField(max_length=255)  # Editable by users
    description = models.TextField(blank=True, null=True)  # Explanation of the permission

    def __str__(self):
        return self.name  # Display the user-defined name in the UI

    class Meta:
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"


class Role(models.Model):
    """Roles as containers for permissions."""
    EMPLOYEE = "Employee"
    MANAGER = "Manager"
    HR_ADMIN = "HR Admin"

    ROLE_CHOICES = [
        (EMPLOYEE, "Employee"),
        (MANAGER, "Manager"),
        (HR_ADMIN, "HR Admin"),
    ]

    name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True, null=True)
    permissions = models.ManyToManyField(PermissionDefinition, blank=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"

    def save(self, *args, **kwargs):
        """Prevent modification of predefined roles."""
        if self.pk:  # Only check when updating
            original = Role.objects.get(pk=self.pk)
            if original.name != self.name:
                raise ValueError("Predefined roles cannot be renamed.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Prevent deletion of predefined roles."""
        raise ValueError("Predefined roles cannot be deleted.")
