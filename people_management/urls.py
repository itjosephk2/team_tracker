from django.urls import path
from . import views

urlpatterns = [
    path('people', views.list_people, name='people'), 
    path('people/<int:pk>', views.view_person, name='view_person'), 
]
