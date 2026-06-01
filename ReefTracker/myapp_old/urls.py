from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    
    
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.sign_up, name='sign_up'),
    path('profile/', views.profile, name='profile'),
    
    path('profile/myaquariums/', views.myaquariums, name='myaquariums'),
    path('profile/myaquariums/<int:aquarium_id>/', views.aquariumview, name='aquariumview'),
    path('profile/myaquariums/<int:aquarium_id>/parameters/', views.parameters, name='parameters'),
    path('profile/myaquariums/<int:aquarium_id>/parameters/data/', views.parameters_data, name='parameters_data'),
    path('profile/myaquariums/<int:aquarium_id>/add_photo/', views.add_photo, name='add_photo'),
    
    path('profile/myaquariums/<int:aquarium_id>/add-livestock/', views.add_livestock, name='add_livestock'),
    path('profile/myaquariums/<int:aquarium_id>/livestock/', views.livestock, name='livestock'),
    
    path('profile/aquarium/<int:aquarium_id>/edit/', views.editaquarium, name='editaquarium'),
    path('delete/<aquarium_id>', views.deleteaquarium, name='deleteaquarium'),
    
    path('calculators/', views.calculators, name='calculators'),
    path('calculators/watervolume', views.watervolumecalc, name='watervolumecalc'),
    path('calculators/calciumdosing', views.calciumcalc, name='calciumcalc'),
    path('calculators/magnesiumdosing', views.magnesiumcalc, name='magnesiumcalc'),
    
]
