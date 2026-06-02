
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
    path('<int:aquarium_id>/target/', views.update_target, name='update_target'),
    
    # Livestock & Media
    path('<int:aquarium_id>/livestock/', views.livestock_list, name='livestock'),
    path('<int:aquarium_id>/add-livestock/', views.add_livestock, name='add_livestock'),
    path('<int:aquarium_id>/add-photo/', views.add_photo, name='add_photo'),
    path('ajax/load-species/', views.load_species, name='ajax_load_species'),
    path('<int:aquarium_id>/livestock/<int:livestock_id>/edit/', views.edit_livestock, name='edit_livestock'),
    path('<int:aquarium_id>/livestock/<int:livestock_id>/delete/', views.delete_livestock, name='delete_livestock'),
    path('<int:aquarium_id>/livestock/<int:livestock_id>/details/', views.livestock_detail, name='livestock_detail'),
    path('<int:aquarium_id>/livestock/<int:livestock_id>/photo/<int:photo_id>/delete/', views.delete_livestock_photo, name='delete_livestock_photo'),
    path('gallery/', views.master_gallery, name='master_gallery'),
    path('tags/quick-add/', views.quick_add_tag, name='quick_add_tag'),
]