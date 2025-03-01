from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListUser.as_view(), name='users'), 
    path('security/<int:pk>/', views.ViewUserDetails.as_view(), name='view_user'),
    path('security/<int:pk>/update_user/', views.UpdateUser.as_view(), name='update_user'),
    path('security/<int:pk>/delete_user/', views.DeleteUser.as_view(), name='delete_user'),
    path('security/create_new_user/', views.CreateNewUser.as_view(), name='create_user'),  
]
