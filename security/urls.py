from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.ListUsers.as_view(), name='users'), 
    path('user/<int:pk>/', views.ViewUserDetails.as_view(), name='view_user'),
    path('user/<int:pk>/update_user/', views.UpdateUser.as_view(), name='update_user'),
    path('user/<int:pk>/delete_user/', views.DeleteUser.as_view(), name='delete_user'),
    path('user/create_new_user/', views.CreateNewUser.as_view(), name='create_user'),  
]
