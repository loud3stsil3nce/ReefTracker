from django import forms
#from django.contrib.auth.models import User
#from django.contrib.auth.forms import UserCreationForm
from .models import Aquariums, WaterParameter, Livestock, Photo, Species, ParameterTarget
from datetime import date
from django.utils import timezone


class AddAquariumForm(forms.ModelForm):
    class Meta:
        model = Aquariums
        fields = ['name', 'size', 'type', 'start_date', 'volume_liters']
        
    start_date = forms.DateField(
        widget=forms.SelectDateWidget(years=range(1900, 2030)), 
        initial=date.today
        )
    volume_liters = forms.FloatField(label="Net Water Volume (L)", required=False, min_value=0)


class AddLivestockForm(forms.ModelForm):
    
    category_filter = forms.ChoiceField(
        choices=[('', 'All Categories')] + Species.CATEGORY_CHOICES,
        required=False,
        label="Filter by Category"
    )
    field_order = ['category_filter', 'species', 'custom_name', 'quantity', 'date_acquired', 'notes', 'image']
    class Meta:
        model = Livestock
        # This tells Django to automatically include every field 
        # except the ones we explicitly exclude below.
        fields = '__all__'
        exclude = ['aquarium', 'created_at', 'updated_at', 'user']
        
        widgets = {
            'date_added': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
class BulkParameterForm(forms.Form):
    # Notice this is forms.Form, NOT forms.ModelForm
    
    measured_at = forms.DateTimeField(
        initial=timezone.now,
        widget=forms.DateTimeInput(
            # This format strictly drops the seconds from the starting value
            format='%Y-%m-%dT%H:%M', 
            attrs={
                'type': 'datetime-local'
                # Notice 'step' is completely gone now!
            }
        ),
        label="Date & Time"
    )
    
    ph = forms.FloatField(required=False, label="pH", widget=forms.NumberInput(attrs={'step': '0.1', 'min': '0'}))
    temp = forms.FloatField(required=False, label="Temperature (°F)", widget=forms.NumberInput(attrs={'step': '0.1', 'min': '0'}))
    salinity = forms.FloatField(required=False, label="Salinity (sg)", widget=forms.NumberInput(attrs={'step': '0.0001', 'min': '1.0000'}))
    
    dkh = forms.FloatField(required=False, label="Alkalinity (dKH)", widget=forms.NumberInput(attrs={'step': '0.1', 'min': '0'}))
    calcium = forms.IntegerField(required=False, label="Calcium (ppm)", widget=forms.NumberInput(attrs={'step': '5', 'min': '0'}))
    magnesium = forms.IntegerField(required=False, label="Magnesium (ppm)", widget=forms.NumberInput(attrs={'step': '10', 'min': '0'}))
    
    nitrate = forms.FloatField(required=False, label="Nitrate (ppm)", widget=forms.NumberInput(attrs={'step': '0.5', 'min': '0'}))
    phosphate = forms.FloatField(required=False, label="Phosphate (ppm)", widget=forms.NumberInput(attrs={'step': '0.01', 'min': '0'}))
    
    ammonia = forms.FloatField(required=False, label="Ammonia (ppm)", widget=forms.NumberInput(attrs={'step': '0.1', 'min': '0'}))
    nitrite = forms.FloatField(required=False, label="Nitrite (ppm)", widget=forms.NumberInput(attrs={'step': '0.1', 'min': '0'}))
    
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2}))
 
 
class ParameterTargetForm(forms.ModelForm):
    class Meta:
        model = ParameterTarget
        fields = ['parameter', 'min_value', 'max_value']
        
        # We add a tiny step so users can input decimals like 8.2 or 0.03
        widgets = {
            'min_value': forms.NumberInput(attrs={'step': '0.0001'}),
            'max_value': forms.NumberInput(attrs={'step': '0.0001'}),
        }



   
class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'caption', 'livestock']

    def __init__(self, *args, **kwargs):
        # We need the aquarium to filter the livestock choices
        aquarium = kwargs.pop('aquarium', None)
        super().__init__(*args, **kwargs)
        
        if aquarium:
            # Only show livestock from the current aquarium as choices
          #  self.fields['livestock'].queryset = aquarium.livestock.all()
          self.fields['livestock'].queryset = aquarium.livestock_items.all()
        
        self.fields['livestock'].required = False
        self.fields['livestock'].label = "Tag Livestock (Optional)"
    