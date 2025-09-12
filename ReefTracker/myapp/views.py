from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .models import Aquariums
# Create your views here.
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegisterForm, WaterVolumeFormImperial, WaterVolumeFormMetric, AddAquariumForm, CalciumDosingCalculatorForm, MagnesiumDosingCalculatorForm
from .utils import inchToCm, cmToInch, inchToFeet, RectangleWaterVolumeCalculator, CalciumDosingCalculator, MagnesiumDosingCalculator
from django.http import JsonResponse
from django.utils import timezone
from .models import WaterParameter
from .forms import WaterParameterForm
import json
def landing(request):
    return render(request, "main/landing.html")
@login_required
def home(request):
    aquariums = Aquariums.objects.filter(user=request.user).only('id', 'user', 'name', 'size', 'type', 'start_date')
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


@login_required
def editaquarium(request, aquarium_id):
    aquarium = get_object_or_404(Aquariums, id=aquarium_id, user=request.user)

    if request.method == 'POST':
        form = AddAquariumForm(request.POST, instance=aquarium)
        if form.is_valid():
            form.save()
            return redirect('myaquariums')
    else:
        form = AddAquariumForm(instance=aquarium)

    return render(request, 'main/editaquarium.html', {'form': form, 'aquarium': aquarium})

@login_required
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
    
    aquariums = Aquariums.objects.filter(user=request.user).only('id', 'user', 'name', 'size', 'type', 'start_date')
    return render(request, "main/myaquariums.html", {
        "aquariums": aquariums,
        "form": form
    })

@login_required
def deleteaquarium(request, aquarium_id):
    if request.method != "POST":
        return redirect("myaquariums")

    aquarium = get_object_or_404(Aquariums, pk=aquarium_id, user=request.user)
    aquarium.delete()
    return redirect("myaquariums")
    

@login_required
def aquariumview(request, aquarium_id):
    
    
    try:
        selectedaquarium = Aquariums.objects.only('id', 'user', 'name', 'size', 'type', 'start_date').get(id=aquarium_id, user=request.user)
    except Aquariums.DoesNotExist:
        return HttpResponse("Aquarium not found.", status=404)
    # recent params (last 3)
    recent_parameters = WaterParameter.objects.filter(aquarium=selectedaquarium).order_by('-measured_at')[:3]
    return render(request, "main/aquariumview.html", {"selectedaquarium": selectedaquarium, "recent_parameters": recent_parameters})


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
            return render(request, "main/watervolume.html", {"form_unit": form_unit, "form": form, "result": result, "totalvolume": totalvolume, "filledvolume": filledvolume, "unit": unit, "result": result})
    else:
        form = WaterVolumeFormImperial() if form_unit == "imperial" else WaterVolumeFormMetric()
    return render(request, "main/watervolume.html", {"form_unit": form_unit, "form": form, "result": result})

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
            return render(request, "main/calciumdosing.html", {"form": form, "result": result, "dosage": dosage if result else None})
            
    else:
        form = CalciumDosingCalculatorForm() 
    return render(request, "main/calciumdosing.html", {"form": form, "result": result, "dosage": None})



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
            return render(request, "main/magnesiumdosing.html", {"form": form, "result": result, "dosage": dosage if result else None})
            
    else:
        form = MagnesiumDosingCalculatorForm() 
    return render(request, "main/magnesiumdosing.html", {"form": form, "result": result, "dosage": None})



@login_required
def parameters(request, aquarium_id):
    aquarium = get_object_or_404(Aquariums, id=aquarium_id, user=request.user)

    if request.method == 'POST':
        form = WaterParameterForm(request.POST)
        if form.is_valid():
            wp = form.save(commit=False)
            wp.aquarium = aquarium
            wp.save()
            return redirect('parameters', aquarium_id=aquarium.id)
    else:
        form = WaterParameterForm()

    # Filters
    parameter_filter = request.GET.get('parameter')
    start = request.GET.get('start')
    end = request.GET.get('end')
    readings = WaterParameter.objects.filter(aquarium=aquarium)
    if parameter_filter:
        readings = readings.filter(parameter=parameter_filter)
    if start:
        readings = readings.filter(measured_at__gte=start)
    if end:
        readings = readings.filter(measured_at__lte=end)

    readings = readings.order_by('-measured_at')

    context = {
        'aquarium': aquarium,
        'form': form,
        'readings': readings[:200],  # cap initial display
        'parameter_filter': parameter_filter or '',
        'start': start or '',
        'end': end or '',
        'allowed_units_json': json.dumps(WaterParameter.ALLOWED_UNITS_BY_PARAMETER),
    }
    return render(request, 'main/parameters.html', context)


@login_required
def parameters_data(request, aquarium_id):
    aquarium = get_object_or_404(Aquariums, id=aquarium_id, user=request.user)
    parameter_key = request.GET.get('parameter')
    start = request.GET.get('start')
    end = request.GET.get('end')
    qs = WaterParameter.objects.filter(aquarium=aquarium)
    if parameter_key:
        qs = qs.filter(parameter=parameter_key)
    if start:
        qs = qs.filter(measured_at__gte=start)
    if end:
        qs = qs.filter(measured_at__lte=end)
    qs = qs.order_by('measured_at')

    labels = [wp.measured_at.isoformat() for wp in qs]
    data = [wp.value for wp in qs]
    unit = qs.first().unit if qs.exists() else ''
    return JsonResponse({
        'labels': labels,
        'datasets': [{
            'label': f"{parameter_key or 'parameter'} ({unit})",
            'data': data,
            'borderColor': '#2388CB',
            'backgroundColor': 'rgba(35,136,203,0.2)'
        }],
        'unit': unit,
    })


