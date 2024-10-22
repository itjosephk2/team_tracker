from django.urls import path
from . import views

urlpatterns = [
    path('people/', views.ListPeopleView.as_view(), name='people'), 
    path('people/<int:pk>', views.ViewPersonDetails.as_view(), name='view_person'),
    path('people/create_new_person', views.CreateNewPerson.as_view(), name='create_person'),  
]
