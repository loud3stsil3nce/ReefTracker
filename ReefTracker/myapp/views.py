from django.shortcuts import render, HttpResponse
from .models import Aquariums
# Create your views here.
from .forms import RegisterForm, LoginForm, WaterVolumeFormImperial, WaterVolumeFormMetric
from .utils import inchToCm, cmToInch, inchToFeet, RectangleWaterVolumeCalculator
def home(request):
    return render(request, "home.html")

def login(request):
    form = LoginForm(request.POST or None)
    return render(request, "login.html", {"form": form})


def register(request):
    form = RegisterForm(request.POST or None)
    return render(request, "register.html", {"form": form})


def profile(request):
    return render(request, "profile.html")

def calculators(request):
    return render(request, "displaycalculators.html")

def myaquariums(request):
    tanks = Aquariums.objects.all()
    return render(request, "myaquariums.html", {"aquariums": tanks})


def watervolumecalc(request):
    result = None
    form_unit = request.POST.get("form_unit", "imperial")
    if request.method == "POST":
        if form_unit == "imperial":
            form = WaterVolumeFormImperial(request.POST)
            unit = "gallons"
        else:
            form = WaterVolumeFormMetric(request.POST)
            unit = "liters"
        if form.is_valid():
            cleaned = form.cleaned_data
            length = cleaned.get("length")
            width = cleaned.get("width")
            height = cleaned.get("height")
            filled_height = cleaned.get("filledheight") or 0
            
            if filled_height > 0:
                filledvolume = RectangleWaterVolumeCalculator(length, width, filled_height, unit=form_unit)
                totalvolume = RectangleWaterVolumeCalculator(length, width, height, unit=form_unit)
            else: 
                totalvolume = RectangleWaterVolumeCalculator(length, width, height, unit=form_unit)
                filledvolume = 0
                
            result = True
            return render(request, "watervolume.html", {"form_unit": form_unit, "form": form, "result": result, "totalvolume": totalvolume, "filledvolume": filledvolume, "unit": unit, "result": result})
    else:
        form = WaterVolumeFormImperial() if form_unit == "imperial" else WaterVolumeFormMetric()
    return render(request, "watervolume.html", {"form_unit": form_unit, "form": form, "result": result})
        