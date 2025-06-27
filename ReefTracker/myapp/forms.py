from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Aquariums
from datetime import date

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    


    
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
    


class AddAquariumForm(forms.ModelForm):
    class Meta:
        model = Aquariums
        fields = ['name', 'size', 'type', 'start_date']
        
    start_date = forms.DateField(
        widget=forms.SelectDateWidget(years=range(1900, 2030)), 
        initial=date.today
        )
    