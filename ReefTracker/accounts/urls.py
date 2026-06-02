app_name = 'accounts'
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Explicitly tell Django where your login template is!
    path('', views.landing, name='landing'),
#    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
  #  path('sign_up/', views.sign_up, name='sign_up'),
   # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]