from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import WaterVolumeFormImperial, WaterVolumeFormMetric, DosingCalculatorForm
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

# --- THE NEW UNIFIED DOSING VIEW ---
def dosing_calculator_view(request):
    result = None
    
    if request.method == 'POST':
        form = DosingCalculatorForm(request.POST)
        if form.is_valid():
            water_volume = form.cleaned_data['waterVolumeMetric']
            current_level = form.cleaned_data['currentPPM']
            target_level = form.cleaned_data['targetPPM']
            product = form.cleaned_data['product'] # This is the DosingProduct database object

            # 1. Calculate the required increase
            increase_needed = target_level - current_level

            # 2. The Chemistry Math
            # Formula: (Volume in L) * (Desired Increase) / (Product PPM per 1ml in 1L)
            dose_in_ml = (water_volume * increase_needed) / product.PPMPerLiter

            # 3. Round to 1 decimal place for a clean UI
            required_dose = round(dose_in_ml, 1)
            
            result = {
                'dose': required_dose,
                'product_name': product.name,
                'category': product.get_category_display(),
                'increase': increase_needed,
            }
    else:
        form = DosingCalculatorForm()

    context = {
        'form': form,
        'result': result
    }
    return render(request, 'calculator/dosing_form.html', context)