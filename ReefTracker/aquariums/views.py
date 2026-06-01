from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.utils import timezone
from django.utils.dateformat import DateFormat
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Aquariums, WaterParameter, Species, Livestock
from .forms import AddLivestockForm, AddAquariumForm, PhotoForm, BulkParameterForm
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
    
    aquarium = get_object_or_404(Aquariums, id=aquarium_id, user=request.user)
    
    
    
    # Get the single most recent reading for EACH parameter type
    latest_readings = WaterParameter.objects.filter(
        aquarium=aquarium
    ).order_by(
        'parameter', 
        '-measured_at'
    ).distinct(
        'parameter'
    )

    # Get the 10 most recent readings overall
    recent_parameters = WaterParameter.objects.filter(
        aquarium=aquarium
    ).order_by('-measured_at')[:10]
    
    total_livestock = aquarium.livestock_items.aggregate(total=Sum('quantity'))['total'] or 0
    fish_count = aquarium.livestock_items.filter(species__category='FISH').aggregate(total=Sum('quantity'))['total'] or 0
    coral_count = aquarium.livestock_items.filter(species__category='CORAL').aggregate(total=Sum('quantity'))['total'] or 0
    invert_count = aquarium.livestock_items.filter(species__category='INVERT').aggregate(total=Sum('quantity'))['total'] or 0
    macro_count = aquarium.livestock_items.filter(species__category='MACRO').aggregate(total=Sum('quantity'))['total'] or 0
    
    context = {
        'aquarium': aquarium,
        'latest_readings': latest_readings,
        'recent_parameters': recent_parameters,

        'total_livestock': total_livestock,
        'fish_count': fish_count,
        'coral_count': coral_count,
        'invert_count': invert_count,
        'macro_count': macro_count,        
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
        # 1. Swap to Bulk Form
        form = BulkParameterForm(request.POST)
        if form.is_valid():
            measured_at = form.cleaned_data.get('measured_at') or timezone.now()
            notes = form.cleaned_data.get('notes', '')

            # 2. Map form fields to your model choices and standard units
            field_mapping = {
                'ph': (WaterParameter.PARAMETER_PH, 'pH'),
                'temp': (WaterParameter.PARAMETER_TEMP, 'F'),
                'salinity': (WaterParameter.PARAMETER_SALINITY, 'sg'),
                'dkh': (WaterParameter.PARAMETER_DKH, 'dKH'),
                'calcium': (WaterParameter.PARAMETER_CALCIUM, 'ppm'),
                'magnesium': (WaterParameter.PARAMETER_MAGNESIUM, 'ppm'),
                'nitrate': (WaterParameter.PARAMETER_NITRATE, 'ppm'),
                'phosphate': (WaterParameter.PARAMETER_PHOSPHATE, 'ppm'),
                'ammonia': (WaterParameter.PARAMETER_AMMONIA, 'ppm'),
                'nitrite': (WaterParameter.PARAMETER_NITRITE, 'ppm'),
            }

            # 3. Loop through and save only the ones the user filled out
            for field, (param_code, unit) in field_mapping.items():
                value = form.cleaned_data.get(field)
                if value is not None:
                    WaterParameter.objects.create(
                        aquarium=aquarium,
                        parameter=param_code,
                        value=value,
                        unit=unit,
                        measured_at=measured_at,
                        notes=notes
                    )
            return redirect('aquariums:parameters', aquarium_id=aquarium.id)
    else:
        form = BulkParameterForm()

    # --- EVERYTHING BELOW THIS LINE STAYS EXACTLY THE SAME ---
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
        # You can remove allowed_units_json since the bulk form hardcodes units!
    }
    return render(request, 'aquariums/parameters.html', context)

@login_required
def parameters_data(request, aquarium_id):
    aquarium = get_object_or_404(Aquariums, id=aquarium_id, user=request.user)
    
    # Get all parameters for this tank, strictly oldest to newest
    qs = aquarium.parameters.all().order_by('measured_at')
    
    # 1. Filters
    param_filter = request.GET.get('parameter')
    if param_filter:
        qs = qs.filter(parameter=param_filter)

    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    if start_date:
        qs = qs.filter(measured_at__gte=start_date)
    if end_date:
        qs = qs.filter(measured_at__lte=end_date)

    # 2. THE FIX: Chronological labels with Time included!
    # By looping through the chronologically ordered queryset, we build a perfect timeline
    labels = []
    for log in qs:
        # Format: "Jun 01, 2026 14:30" (Includes Hours and Minutes)
        date_str = log.measured_at.strftime('%b %d, %Y %H:%M')
        if date_str not in labels:
            labels.append(date_str)

    # 3. Group the data by Parameter Type
    grouped_data = {}
    for log in qs:
        param_name = log.get_parameter_display()
        date_str = log.measured_at.strftime('%b %d, %Y %H:%M')
        
        if param_name not in grouped_data:
            grouped_data[param_name] = {}
            
        grouped_data[param_name][date_str] = log.value

    # 4. Build the "datasets" array (This part stays exactly the same)
    datasets = []
    colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#E7E9ED']
    
    for index, (param_name, date_values) in enumerate(grouped_data.items()):
        data_array = []
        for label in labels:
            data_array.append(date_values.get(label, None))
            
        datasets.append({
            'label': param_name,
            'data': data_array,
            'borderColor': colors[index % len(colors)],
            'backgroundColor': colors[index % len(colors)],
            'spanGaps': True,
            'tension': 0.3
        })

    # NEW: 5. Build the Target Zones Dictionary
    # These are the default fallback values
    target_zones = {
        'ph': {'min': 8.0, 'max': 8.4},
        'temp': {'min': 77, 'max': 80},
        'salinity': {'min': 1.024, 'max': 1.026},
        'dkh': {'min': 8.0, 'max': 11.5},
        'calcium': {'min': 400, 'max': 450},
        'magnesium': {'min': 1250, 'max': 1400},
        'nitrate': {'min': 2.0, 'max': 10.0},
        'phosphate': {'min': 0.03, 'max': 0.1}
    }
    
    # Check the database for custom user targets and override the defaults!
    custom_targets = aquarium.target_zones.all()
    for custom in custom_targets:
        target_zones[custom.parameter] = {
            'min': custom.min_value, 
            'max': custom.max_value
        }

    # Include target_zones in the JSON response
    return JsonResponse({
        'labels': labels,
        'datasets': datasets,
        'target_zones': target_zones
    })
     
    

    
@login_required
def add_parameter_log(request, aquarium_id):
    aquarium = get_object_or_404(Aquariums, id=aquarium_id, user=request.user)
    
    if request.method == "POST":
        form = BulkParameterForm(request.POST)
        if form.is_valid():
            measured_at = form.cleaned_data.get('measured_at') or timezone.now()
            notes = form.cleaned_data.get('notes', '')
            
            # This maps your form fields to your exact model choices and units!
            field_mapping = {
                'ph': (WaterParameter.PARAMETER_PH, 'pH'),
                'temp': (WaterParameter.PARAMETER_TEMP, 'F'), 
                'salinity': (WaterParameter.PARAMETER_SALINITY, 'sg'),
                'dkh': (WaterParameter.PARAMETER_DKH, 'dKH'),
                'calcium': (WaterParameter.PARAMETER_CALCIUM, 'ppm'),
                'magnesium': (WaterParameter.PARAMETER_MAGNESIUM, 'ppm'),
                'nitrate': (WaterParameter.PARAMETER_NITRATE, 'ppm'),
                'phosphate': (WaterParameter.PARAMETER_PHOSPHATE, 'ppm'),
                'ammonia': (WaterParameter.PARAMETER_AMMONIA, 'ppm'),
                'nitrite': (WaterParameter.PARAMETER_NITRITE, 'ppm'),
            }
            
            # Loop through the map. If they typed a number, save the row!
            for field, (param_code, unit) in field_mapping.items():
                value = form.cleaned_data.get(field)
                if value is not None:
                    WaterParameter.objects.create(
                        aquarium=aquarium,
                        parameter=param_code,
                        value=value,
                        unit=unit,
                        measured_at=measured_at,
                        notes=notes
                    )
                    
            # Send them back to the dashboard when done
            return redirect('aquariums:aquariumview', aquarium_id=aquarium.id)
    else:
        form = BulkParameterForm()
        
    return render(request, "aquariums/add_parameters.html", {
        "form": form,
        "aquarium": aquarium
    })

@login_required
def livestock_list(request, aquarium_id):
    aquarium = get_object_or_404(Aquariums, id=aquarium_id, user=request.user)
    
    # Actually fetch the fish and corals!
    inhabitants = aquarium.livestock_items.all().select_related('species').order_by('-date_acquired')
    
    context = {
        'aquarium': aquarium, 
        'inhabitants': inhabitants
    }
    return render(request, 'aquariums/livestock_list.html', context)


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
def edit_livestock(request, aquarium_id, livestock_id):
    # 1. Secure the aquarium
    aquarium = get_object_or_404(Aquariums, id=aquarium_id, user=request.user)
    # 2. Get the specific livestock item, ensuring it belongs to THIS aquarium
    livestock_item = get_object_or_404(Livestock, id=livestock_id, aquarium=aquarium)
    
    if request.method == "POST":
        # Pass instance=livestock_item so Django knows we are UPDATING, not creating
        form = AddLivestockForm(request.POST, request.FILES, instance=livestock_item)
        if form.is_valid():
            form.save()
            return redirect('aquariums:livestock', aquarium_id=aquarium.id)
    else:
        # Pre-fill the form with the existing data
        form = AddLivestockForm(instance=livestock_item)
        
    return render(request, "aquariums/edit_livestock.html", {
        "form": form,
        "aquarium": aquarium,
        "livestock_item": livestock_item
    })

@login_required
def delete_livestock(request, aquarium_id, livestock_id):
    aquarium = get_object_or_404(Aquariums, id=aquarium_id, user=request.user)
    livestock_item = get_object_or_404(Livestock, id=livestock_id, aquarium=aquarium)
    
    # We require a POST request to actually delete data (security best practice)
    if request.method == "POST":
        livestock_item.delete()
        return redirect('aquariums:livestock', aquarium_id=aquarium.id)
        
    return render(request, "aquariums/delete_livestock.html", {
        "aquarium": aquarium,
        "livestock_item": livestock_item
    })


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




@login_required
def load_species(request):
    category = request.GET.get('category')
    
    if category:
        species = Species.objects.filter(category=category).order_by('common_name')
    else:
        species = Species.objects.all(). order_by('common_name')
        
    species_list = list(species.values('id', 'common_name'))
    return JsonResponse(species_list, safe=False)  
