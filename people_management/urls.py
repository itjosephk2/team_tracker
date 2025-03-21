from django.urls import path
from . import views

app_name = 'people_management'

urlpatterns = [
    path('people/', views.ListPeople.as_view(), name='people'), 
    path('people/<int:pk>/', views.ViewPersonDetails.as_view(), name='view_person'),
    path('me/', views.ViewOwnPerson.as_view(), name='view_own_person'),
    path('people/<int:pk>/update_person/', views.UpdatePerson.as_view(), name='update_person'),
    path('people/<int:pk>/delete_person/', views.DeletePerson.as_view(), name='delete_person'),
    path('people/create_new_person/', views.CreateNewPerson.as_view(), name='create_person'),  
    path('contracts/', views.FilteredContractListView.as_view(), name='contracts'),
    path('contracts/<int:pk>/', views.ViewContractDetails.as_view(), name='view_contract'),
    path('contracts/<int:pk>/update_contract/', views.UpdateContract.as_view(), name='update_contract'),
    path('contracts/<int:pk>/delete_contract/', views.DeleteContract.as_view(), name='delete_contract'),
    path('contracts/create_new_contract/', views.CreateNewContract.as_view(), name='create_contract'), 
]
