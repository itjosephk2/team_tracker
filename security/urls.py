from django.urls import path
from django.contrib.auth import views as auth_views  # Built-in Django auth views
from . import views

app_name = "security"

urlpatterns = [
    # Authentication URLs
    path('login/', views.LoginInterface.as_view(), name='login'),
    path('logout/', views.LogoutInterface.as_view(), name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),

    # Password Reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # User Management
    path("users/", views.ListUsers.as_view(), name="user_list"),
    path("users/<int:pk>/", views.ViewUserDetails.as_view(), name="user_detail"),
    path("users/edit/<int:pk>/", views.UpdateUser.as_view(), name="user_edit"),
    path("users/delete/<int:pk>/", views.DeleteUser.as_view(), name="user_delete"),
    path("users/add/", views.CreateNewUser.as_view(), name="user_create"),

    # Group Management
    path("groups/", views.group_list, name="group_list"),
    path("groups/add/", views.group_edit, name="group_add"),
    path("groups/edit/<int:pk>/", views.group_edit, name="group_edit"),
    path("groups/delete/<int:pk>/", views.group_delete, name="group_delete"),
]
