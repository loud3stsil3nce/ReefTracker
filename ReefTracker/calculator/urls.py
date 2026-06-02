from django.urls import path
from . import views

urlpatterns = [
    # We will paste your actual paths here soon!
    path('', views.calculators, name='calculators'),
    path('watervolume/', views.watervolumecalc, name='watervolumecalc'),
    # The NEW unified dosing URL
    path('dosing/', views.dosing_calculator_view, name='dosing_calculator'),
    
]