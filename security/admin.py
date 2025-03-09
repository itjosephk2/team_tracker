from django.contrib import admin
from security.models import Role, PermissionDefinition


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "description")  # Fields to show in the list view
    search_fields = ("name",)  # Enables search by name
    filter_horizontal = ("permissions",)  # Enables better permission selection in the UI


@admin.register(PermissionDefinition)
class PermissionDefinitionAdmin(admin.ModelAdmin):
    list_display = ("codename", "name", "description")  # Fields to show in the list view
    search_fields = ("codename", "name")  # Enables search by codename or name
