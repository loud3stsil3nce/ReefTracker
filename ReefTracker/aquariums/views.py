from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Aquariums, WaterParameter
from .forms import AddLivestockForm, WaterParameterForm, AddAquariumForm, PhotoForm
import json


@login_required
def myaquariums(request):
    if request.method == "POST":
        form = AddAquariumForm(request.POST)
        if form.is_valid():
            aquarium = form.save(commit=False)
            aquarium.user = request.user
            aquarium.save()
            return redirect("aquariums:myaquariums")  # prevent form resubmission
    else:
        form = AddAquariumForm()
    
    aquariums = Aquariums.objects.filter(user=request.user).only('id', 'user', 'name', 'size', 'type', 'start_date')
    return render(request, "aquariums/myaquariums.html", {
        "aquariums": aquariums,
        "form": form
    })
    
@login_required
def editaquarium(request, aquarium_id):
    aquarium = get_object_or_404(Aquariums, id=aquarium_id, user=request.user)

    if request.method == 'POST':
        form = AddAquariumForm(request.POST, instance=aquarium)
        if form.is_valid():
            form.save()
            return redirect('aquariums:myaquariums')
    else:
        form = AddAquariumForm(instance=aquarium)

    return render(request, 'aquariums/editaquarium.html', {'form': form, 'aquarium': aquarium})


@login_required
def aquariumview(request, aquarium_id):
    
    selectedaquarium = get_object_or_404(Aquariums, id=aquarium_id, user=request.user)
    
    # Get the single most recent reading for EACH parameter type
    latest_readings = WaterParameter.objects.filter(
        aquarium=selectedaquarium
    ).order_by(
        'parameter', 
        '-measured_at'
    ).distinct(
        'parameter'
    )

    # Get the 10 most recent readings overall
    recent_parameters = WaterParameter.objects.filter(
        aquarium=selectedaquarium
    ).order_by('-measured_at')[:10]

    context = {
        'aquarium': selectedaquarium,
        'latest_readings': latest_readings,
        'recent_parameters': recent_parameters,
    }
    
    
    return render(request, "aquariums/aquariumview.html", context)


@login_required
def deleteaquarium(request, aquarium_id):
    if request.method != "POST":
        return redirect("aquariums:myaquariums")

    aquarium = get_object_or_404(Aquariums, pk=aquarium_id, user=request.user)
    aquarium.delete()
    return redirect("aquariums:myaquariums")
    

@login_required
def parameters(request, aquarium_id):
    aquarium = get_object_or_404(Aquariums, id=aquarium_id, user=request.user)

    if request.method == 'POST':
        form = WaterParameterForm(request.POST)
        if form.is_valid():
            wp = form.save(commit=False)
            wp.aquarium = aquarium
            wp.save()
            return redirect('aquariums:parameters', aquarium_id=aquarium.id)
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
    return render(request, 'aquariums/parameters.html', context)


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


@login_required
def livestock(request, aquarium_id):
    aquarium = get_object_or_404(Aquariums, id=aquarium_id, user=request.user)
    
    # Actually fetch the fish and corals!
    inhabitants = aquarium.livestock_items.all().select_related('species').order_by('-date_acquired')
    
    context = {
        'aquarium': aquarium, 
        'inhabitants': inhabitants
    }
    return render(request, 'aquariums/livestock.html', context)


@login_required
def add_livestock(request, aquarium_id):
    # Securely fetch the aquarium, ensuring it belongs to the logged-in user
    aquarium = get_object_or_404(Aquariums, id=aquarium_id, user=request.user)

    if request.method == 'POST':
        form = AddLivestockForm(request.POST, request.FILES)
        if form.is_valid():
            # Create the Livestock object, but DON'T save it to the DB just yet
            new_livestock = form.save(commit=False)
            
            # Manually attach the secure backend data
            new_livestock.user = request.user
            new_livestock.aquarium = aquarium
            
            # Now commit to PostgreSQL
            new_livestock.save()
            
            # Redirect back to the aquarium's dashboard (we'll assume you have a view for this)
            return redirect('aquariums:livestock', aquarium_id=aquarium.id)
    else:
        form = AddLivestockForm()

    context = {
        'form': form,
        'aquarium': aquarium
    }
    return render(request, 'aquariums/add_livestock.html', context)

@login_required
def add_photo(request, aquarium_id):
    aquarium = get_object_or_404(Aquariums, id=aquarium_id, user=request.user)
    
    if request.method == 'POST':
        # Pass the aquarium object to the form
        form = PhotoForm(request.POST, request.FILES, aquarium=aquarium)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.aquarium = aquarium
            photo.save()
            return redirect('aquariums:aquariumview', aquarium_id=aquarium.id) # Redirect to aquarium detail page
    else:
        form = PhotoForm(aquarium=aquarium) # Pass aquarium for filtering
        
    return render(request, 'aquariums/add_photo.html', {'form': form, 'aquarium': aquarium})

