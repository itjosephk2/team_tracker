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
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    permissions = models.ManyToManyField(PermissionDefinition, blank=True)
    is_default = models.BooleanField(default=False)  # Prevent deletion/editing of system roles

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"

    def save(self, *args, **kwargs):
        """Prevent modification of default roles."""
        if self.is_default and self.pk:
            original = Role.objects.get(pk=self.pk)
            if original.name != self.name or original.description != self.description or set(original.permissions.all()) != set(self.permissions.all()):
                raise ValueError("Default roles cannot be modified.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Prevent deletion of default roles but allow deletion of custom roles."""
        if self.is_default:
            raise ValueError("Default roles cannot be deleted.")
        super().delete(*args, **kwargs)
