from django.urls import path
from . import views

urlpatterns = [
    path('people/', views.ListPeople.as_view(), name='people'), 
    path('people/<int:pk>', views.ViewPersonDetails.as_view(), name='view_person'),
    path('people/<int:pk>/update_person', views.UpdatePerson.as_view(), name='update_person'),
    path('people/<int:pk>/delete_person', views.DeletePerson.as_view(), name='delete_person'),
    path('people/create_new_person', views.CreateNewPerson.as_view(), name='create_person'),  
    path('contracts/', views.ListContracts.as_view(), name='contracts'), 
    path('contracts/<int:pk>', views.ViewContractDetails.as_view(), name='view_contract'),
    path('contracts/<int:pk>/update_contract', views.UpdateContract.as_view(), name='update_contract'),
    path('contracts/<int:pk>/delete_contract', views.DeteContract.as_view(), name='delete_contract'),
    path('contracts/create_new_contract', views.CreateNewContract.as_view(), name='create_contract'),  
]
