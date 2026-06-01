from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import WaterVolumeFormImperial, WaterVolumeFormMetric, CalciumDosingCalculatorForm, MagnesiumDosingCalculatorForm
from .utils import inchToCm, cmToInch, inchToFeet, RectangleWaterVolumeCalculator, CalciumDosingCalculator, MagnesiumDosingCalculator


# Create your views here.
@login_required
def calculators(request):
    return render(request, "calculator/displaycalculators.html")

@login_required
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
            return render(request, "calculator/watervolume.html", {"form_unit": form_unit, "form": form, "result": result, "totalvolume": totalvolume, "filledvolume": filledvolume, "unit": unit, "result": result})
    else:
        form = WaterVolumeFormImperial() if form_unit == "imperial" else WaterVolumeFormMetric()
    return render(request, "calculator/watervolume.html", {"form_unit": form_unit, "form": form, "result": result})

@login_required        
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
            return render(request, "calculator/calciumdosing.html", {"form": form, "result": result, "dosage": dosage if result else None})
            
    else:
        form = CalciumDosingCalculatorForm() 
    return render(request, "calculator/calciumdosing.html", {"form": form, "result": result, "dosage": None})



@login_required
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
            return render(request, "calculator/magnesiumdosing.html", {"form": form, "result": result, "dosage": dosage if result else None})
            
    else:
        form = MagnesiumDosingCalculatorForm() 
    return render(request, "calculator/magnesiumdosing.html", {"form": form, "result": result, "dosage": None})
