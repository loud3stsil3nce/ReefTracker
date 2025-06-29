from django.shortcuts import render, redirect, HttpResponse
from .models import Aquariums
# Create your views here.
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegisterForm, WaterVolumeFormImperial, WaterVolumeFormMetric, AddAquariumForm, CalciumDosingCalculatorForm, MagnesiumDosingCalculatorForm
from .utils import inchToCm, cmToInch, inchToFeet, RectangleWaterVolumeCalculator, CalciumDosingCalculator, MagnesiumDosingCalculator
def landing(request):
    return render(request, "main/landing.html")
@login_required
def home(request):
    aquariums = Aquariums.objects.filter(user=request.user)
    if request.method == "POST":
        form = AddAquariumForm(request.POST)
        if form.is_valid():
            aquarium = form.save(commit=False)
            aquarium.user = request.user
            aquarium.save()
            return redirect("home")  # prevent form resubmission
    else:
        form = AddAquariumForm()
    return render(request, "main/home.html", {"aquariums": aquariums, "form": form})


def sign_up(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, "registration/sign_up.html", {"form": form})

@login_required
def profile(request):
    return render(request, "main/profile.html")

def calculators(request):
    return render(request, "main/displaycalculators.html")

@login_required
def myaquariums(request):
    if request.method == "POST":
        form = AddAquariumForm(request.POST)
        if form.is_valid():
            aquarium = form.save(commit=False)
            aquarium.user = request.user
            aquarium.save()
            return redirect("myaquariums")  # prevent form resubmission
    else:
        form = AddAquariumForm()
    
    aquariums = Aquariums.objects.filter(user=request.user)
    return render(request, "main/myaquariums.html", {
        "aquariums": aquariums,
        "form": form
    })

@login_required
def aquariumview(request, aquarium_id):
    
    
    try:
        selectedaquarium = Aquariums.objects.get(id=aquarium_id, user=request.user)
    except Aquariums.DoesNotExist:
        return HttpResponse("Aquarium not found.", status=404)
    
    return render(request, "main/aquariumview.html", {"selectedaquarium": selectedaquarium})

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
                filledvolume = round(RectangleWaterVolumeCalculator(length, width, filled_height, unit=form_unit), 2)
                totalvolume = round(RectangleWaterVolumeCalculator(length, width, height, unit=form_unit), 2)
            else: 
                totalvolume = round(RectangleWaterVolumeCalculator(length, width, height, unit=form_unit), 2)
                filledvolume = 0.00
                
            result = True
            return render(request, "main/watervolume.html", {"form_unit": form_unit, "form": form, "result": result, "totalvolume": totalvolume, "filledvolume": filledvolume, "unit": unit, "result": result})
    else:
        form = WaterVolumeFormImperial() if form_unit == "imperial" else WaterVolumeFormMetric()
    return render(request, "main/watervolume.html", {"form_unit": form_unit, "form": form, "result": result})
        
def calciumcalc(request):
    result = None
    
    if request.method == "POST":
        form = CalciumDosingCalculatorForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            product = cleaned.get("product")
            currentPPM = float(cleaned.get("currentPPM"))
            targetPPM = float(cleaned.get("targetPPM"))
            waterVolumeL = float(cleaned.get("waterVolumeMetric"))
            solutionPPM = float(product.PPMPerLiter)
            
            ppmIncrease = targetPPM - currentPPM
            dosage = round(CalciumDosingCalculator(ppmIncrease, waterVolumeL, solutionPPM), 2)
            result = True
            return render(request, "main/calciumdosing.html", {"form": form, "result": result, "dosage": dosage if result else None})
            
    else:
        form = CalciumDosingCalculatorForm() 
    return render(request, "main/calciumdosing.html", {"form": form, "result": result, "dosage": None})

def magnesiumcalc(request):
    result = None
    
    if request.method == "POST":
        form = MagnesiumDosingCalculatorForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            product = cleaned.get("product")
            currentPPM = float(cleaned.get("currentPPM"))
            targetPPM = float(cleaned.get("targetPPM"))
            waterVolumeL = float(cleaned.get("waterVolumeMetric"))
            solutionPPM = float(product.PPMPerLiter)
            
            ppmIncrease = targetPPM - currentPPM
            dosage = round(MagnesiumDosingCalculator(ppmIncrease, waterVolumeL, solutionPPM), 2)
            result = True
            return render(request, "main/magnesiumdosing.html", {"form": form, "result": result, "dosage": dosage if result else None})
            
    else:
        form = MagnesiumDosingCalculatorForm() 
    return render(request, "main/magnesiumdosing.html", {"form": form, "result": result, "dosage": None})