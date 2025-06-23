from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('login', views.login, name='login'),
    path('profile', views.profile, name='profile'),
    path('calculators', views.calculators, name='calculators'),
    path('profile/myaquariums', views.myaquariums, name='myaquariums')
]
