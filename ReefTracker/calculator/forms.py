# calculator/forms.py
from django import forms
from django.utils import timezone
from datetime import date

# Import the NEW unified model
from .models import DosingProduct

# --- KEEP YOUR WATER VOLUME FORMS EXACTLY AS THEY ARE ---
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

# --- THE NEW UNIFIED DOSING FORM ---
class DosingCalculatorForm(forms.Form):
    # The dropdown that pulls every product from your database automatically
    product = forms.ModelChoiceField(
        queryset=DosingProduct.objects.all(),
        empty_label="--- Select a Product ---",
        to_field_name="name"
    )
    
    # We can use the same fields you already designed!
    currentPPM = forms.FloatField(label="Current Level", min_value=0)
    targetPPM = forms.FloatField(label="Target Level", min_value=0)
    
    # Keeping your metric standard
    waterVolumeMetric = forms.FloatField(label="Net Water Volume in Liters", min_value=0)

    # Added a quick validation check so users can't accidentally calculate a negative dose
    def clean(self):
        cleaned_data = super().clean()
        current = cleaned_data.get('currentPPM')
        target = cleaned_data.get('targetPPM')

        if current and target and current >= target:
            raise forms.ValidationError("Target level must be higher than the current level.")
            
        return cleaned_data  
    
    