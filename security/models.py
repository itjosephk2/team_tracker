from django.db import models
from django.core.exceptions import ValidationError


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

    PREDEFINED_ROLES = {EMPLOYEE, MANAGER, HR_ADMIN}  # Set for quick lookups

    name = models.CharField(max_length=50, unique=True)  # Removed choices to allow custom roles
    description = models.TextField(blank=True, null=True)
    permissions = models.ManyToManyField(PermissionDefinition, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"

    def clean(self):
        """Prevent renaming predefined roles."""
        if self.pk:
            original = Role.objects.get(pk=self.pk)
            if original.name in self.PREDEFINED_ROLES and original.name != self.name:
                raise ValidationError("Predefined roles cannot be renamed.")

    def save(self, *args, **kwargs):
        """Ensure predefined roles cannot be renamed."""
        self.clean()  # Validate before saving
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Prevent deletion of predefined roles."""
        if self.name in self.PREDEFINED_ROLES:
            raise ValidationError("Predefined roles cannot be deleted.")
        super().delete(*args, **kwargs)
