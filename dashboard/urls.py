from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name="dashboard"),
    path('authorized/', views.AuthorizedView.as_view(), name='authorized'),
    path('login/', views.LoginInterface.as_view(), name='login'),
    path('logout/', views.LogoutInterface.as_view(), name='logout'),
]
