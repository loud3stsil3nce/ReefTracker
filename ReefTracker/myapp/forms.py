from django import forms

class RegisterForm(forms.Form):
    username =  forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    
class WaterVolumeFormMetric(forms.Form):
    length = forms.FloatField(label="Length (cm)")
    width = forms.FloatField(label="Width (cm)")
    height = forms.FloatField(label="Height (cm)")
    filledheight = forms.FloatField(label="Filled Height (cm)", required=False)

class WaterVolumeFormImperial(forms.Form):
    length = forms.FloatField(label="Length (inches)")
    width = forms.FloatField(label="Width (inches)")
    height = forms.FloatField(label="Height (inches)")
    filledheight = forms.FloatField(label="Filled Height (inches)", required=False)
    
