from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    LoginInterface, LogoutInterface, SignupView,
    ListUsers, ViewUserDetails, UpdateUser, DeleteUser, CreateNewUser,
    ListGroups, GroupDetailView, CreateGroup, UpdateGroup, DeleteGroup
)

app_name = "security"

urlpatterns = [
    # Authentication URLs
    path('login/', LoginInterface.as_view(), name='login'),
    path('logout/', LogoutInterface.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),

    # # Password Reset URLs
    # path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # User Management
    path("users/", ListUsers.as_view(), name="user_list"),
    path("users/<int:pk>/", ViewUserDetails.as_view(), name="user_detail"),
    path("users/edit/<int:pk>/", UpdateUser.as_view(), name="user_edit"),
    path("users/delete/<int:pk>/", DeleteUser.as_view(), name="user_delete"),
    path("users/add/", CreateNewUser.as_view(), name="user_create"),

    # Group Management (Updated to Class-Based Views)
    path("groups/", ListGroups.as_view(), name="group_list"),
    path("groups/<int:pk>/", GroupDetailView.as_view(), name="group_detail"),
    path("groups/add/", CreateGroup.as_view(), name="group_add"),
    path("groups/edit/<int:pk>/", UpdateGroup.as_view(), name="group_edit"),
    path("groups/delete/<int:pk>/", DeleteGroup.as_view(), name="group_delete"),
]
