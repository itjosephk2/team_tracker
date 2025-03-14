from django.urls import path
from . import views

app_name = "security"  # Namespace for security app

urlpatterns = [
    # User Management URLs
    path("users/", views.ListUsers.as_view(), name="user_list"),  # List all users
    path("users/<int:pk>/", views.ViewUserDetails.as_view(), name="user_detail"),  # View user details
    path("users/edit/<int:pk>/", views.UpdateUser.as_view(), name="user_edit"),  # Edit user
    path("users/delete/<int:pk>/", views.DeleteUser.as_view(), name="user_delete"),  # Delete user
    path("users/add/", views.CreateNewUser.as_view(), name="user_create"),  # Create new user
    
    # Group Management URLs
    path("groups/", views.group_list, name="group_list"),  # List all groups
    path("groups/add/", views.group_edit, name="group_add"),  # Add new group
    path("groups/edit/<int:pk>/", views.group_edit, name="group_edit"),  # Edit existing group
    path("groups/delete/<int:pk>/", views.group_delete, name="group_delete"),  # Delete group
]
