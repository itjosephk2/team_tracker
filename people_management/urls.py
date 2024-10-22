from django.urls import path
from . import views

urlpatterns = [
    path('people/', views.ListPeopleView.as_view(), name='people'), 
    path('people/<int:pk>', views.ViewPersonDetails.as_view(), name='view_person'), 
]
