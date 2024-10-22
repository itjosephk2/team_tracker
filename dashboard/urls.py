from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name="dashboard"),
    path('authorized/', views.AuthorizedView.as_view(), name='authorized'),
]
