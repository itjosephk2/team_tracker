from django.urls import path
from . import views

app_name = "security"  # Namespace for security app

urlpatterns = [
    # User Management URLs
    path("users/", views.ListUsers.as_view(), name="user_list"),  # List all users
    path("user/<int:pk>/", views.ViewUserDetails.as_view(), name="user_detail"),  # View user details
    path("user/<int:pk>/edit/", views.UpdateUser.as_view(), name="user_edit"),  # Edit user
    path("user/<int:pk>/delete/", views.DeleteUser.as_view(), name="user_delete"),  # Delete user
    path("user/create/", views.CreateNewUser.as_view(), name="user_create"),  # Create new user
]
