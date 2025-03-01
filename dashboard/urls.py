from django.urls import path
from django.contrib.auth import views as auth_views  # <-- This is the missing import
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name="dashboard"),
    path('login/', views.LoginInterface.as_view(), name='login'),
    path('logout/', views.LogoutInterface.as_view(), name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    # Password Reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
