from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register', views.sign_up, name='sign_up'),  
    path('profile', views.profile, name='profile'),
    path('calculators', views.calculators, name='calculators'),
    path('calculators/watervolume', views.watervolumecalc, name='watervolumecalc'),
    path('profile/myaquariums', views.myaquariums, name='myaquariums'),
    
]
