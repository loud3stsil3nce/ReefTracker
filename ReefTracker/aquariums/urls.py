
from django.urls import path
from . import views
app_name = 'aquariums'
urlpatterns = [
    # List of all aquariums
    path('', views.myaquariums, name='myaquariums'),
    
    # Detail and CRUD operations
    path('<int:aquarium_id>/', views.aquariumview, name='aquariumview'),
    path('<int:aquarium_id>/edit/', views.editaquarium, name='editaquarium'),
    path('<int:aquarium_id>/delete/', views.deleteaquarium, name='deleteaquarium'),
    
    # Parameters
    path('<int:aquarium_id>/parameters/', views.parameters, name='parameters'),
    path('<int:aquarium_id>/parameters/data/', views.parameters_data, name='parameters_data'),
    
    # Livestock & Media
    path('<int:aquarium_id>/livestock/', views.livestock, name='livestock'),
    path('<int:aquarium_id>/add-livestock/', views.add_livestock, name='add_livestock'),
    path('<int:aquarium_id>/add-photo/', views.add_photo, name='add_photo'),
]