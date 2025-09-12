from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Aquariums, CalciumProducts, MagnesiumProducts, WaterParameter
from datetime import date
from django.utils import timezone

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
    
    

class AddAquariumForm(forms.ModelForm):
    class Meta:
        model = Aquariums
        fields = ['name', 'size', 'type', 'start_date', 'volume_liters']
        
    start_date = forms.DateField(
        widget=forms.SelectDateWidget(years=range(1900, 2030)), 
        initial=date.today
        )
    volume_liters = forms.FloatField(label="Net Water Volume (L)", required=False, min_value=0)


class WaterParameterForm(forms.ModelForm):
    parameter = forms.ChoiceField(choices=WaterParameter.PARAMETER_CHOICES, label="Parameter")
    unit = forms.ChoiceField(choices=[], label="Unit")
    measured_at = forms.DateTimeField(
        label="Measured At",
        initial=timezone.now,
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
        required=True,
    )

    class Meta:
        model = WaterParameter
        fields = ["parameter", "value", "unit", "measured_at", "notes"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set unit choices based on provided parameter from data or instance
        parameter_key = None
        if self.data.get("parameter"):
            parameter_key = self.data.get("parameter")
        elif self.initial.get("parameter"):
            parameter_key = self.initial.get("parameter")
        elif self.instance and self.instance.pk:
            parameter_key = self.instance.parameter

        allowed = WaterParameter.ALLOWED_UNITS_BY_PARAMETER.get(parameter_key) if parameter_key else None
        self.fields["unit"].choices = allowed or [("", "Select a unit")]

    def clean(self):
        cleaned = super().clean()
        parameter_key = cleaned.get("parameter")
        unit = cleaned.get("unit")
        value = cleaned.get("value")

        # Validate unit against parameter
        allowed_pairs = WaterParameter.ALLOWED_UNITS_BY_PARAMETER.get(parameter_key, [])
        allowed_values = {code for code, _ in allowed_pairs}
        if parameter_key and unit and unit not in allowed_values:
            self.add_error("unit", f"Unit '{unit}' not allowed for parameter '{parameter_key}'.")

        # Bounds by parameter (basic sensible defaults for reefs)
        bounds = {
            WaterParameter.PARAMETER_PH: (6.0, 9.0),
            WaterParameter.PARAMETER_TEMP: (10.0, 35.0),
            WaterParameter.PARAMETER_SALINITY: (1.0, 40.0),  # accepts sg/ppt/psu; validated loosely here
            WaterParameter.PARAMETER_DKH: (0.0, 20.0),
            WaterParameter.PARAMETER_CALCIUM: (200.0, 600.0),
            WaterParameter.PARAMETER_MAGNESIUM: (800.0, 1800.0),
            WaterParameter.PARAMETER_NITRATE: (0.0, 500.0),
            WaterParameter.PARAMETER_PHOSPHATE: (0.0, 10.0),
            WaterParameter.PARAMETER_AMMONIA: (0.0, 10.0),
            WaterParameter.PARAMETER_NITRITE: (0.0, 10.0),
        }
        if parameter_key in bounds and value is not None:
            low, high = bounds[parameter_key]
            if not (low <= value <= high):
                self.add_error("value", f"Value out of expected range [{low}, {high}].")

        return cleaned
    