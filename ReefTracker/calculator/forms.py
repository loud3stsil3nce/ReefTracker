from django import forms
from django.utils import timezone

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import CalciumProducts, MagnesiumProducts

from datetime import date


    
class WaterVolumeFormMetric(forms.Form):
    length = forms.FloatField(label="Length")
    width = forms.FloatField(label="Width")
    height = forms.FloatField(label="Height")
    filledheight = forms.FloatField(label="Filled Height", required=False)

class WaterVolumeFormImperial(forms.Form):
    length = forms.FloatField(label="Length")
    width = forms.FloatField(label="Width")
    height = forms.FloatField(label="Height")
    filledheight = forms.FloatField(label="Filled Height", required=False)
    
class CalciumDosingCalculatorForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=CalciumProducts.objects.all(),
        empty_label="Select a Product",
        to_field_name="name"
    )
    currentPPM = forms.FloatField(label="Current Level in PPM", min_value=0)
    targetPPM = forms.FloatField(label="Target Level in PPM", min_value=0)
    waterVolumeMetric = forms.FloatField(label="Net Water Volume in Liters", min_value=0)  
    
    
class MagnesiumDosingCalculatorForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=MagnesiumProducts.objects.all(),
        empty_label="Select a Product",
        to_field_name="name"
    )
    currentPPM = forms.FloatField(label="Current Level in PPM", min_value=0)
    targetPPM = forms.FloatField(label="Target Level in PPM", min_value=0)
    waterVolumeMetric = forms.FloatField(label="Net Water Volume in Liters", min_value=0)  
    
    