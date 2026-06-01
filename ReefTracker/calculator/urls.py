from django.urls import path
from . import views

urlpatterns = [
    # We will paste your actual paths here soon!
    path('', views.calculators, name='calculators'),
    path('watervolume/', views.watervolumecalc, name='watervolumecalc'),
    path('calciumdosing/', views.calciumcalc, name='calciumcalc'),
    path('magnesiumdosing/', views.magnesiumcalc, name='magnesiumcalc'),
    
]