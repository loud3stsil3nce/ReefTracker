from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from itertools import chain
from operator import attrgetter
import time
from .forms import RegisterForm, UserEditForm
from aquariums.models import Aquariums, WaterParameter, Livestock, Photo, ParameterTarget
from aquariums.forms import AddAquariumForm


def landing(request):
    return render(request, "landing.html")

@login_required
def home(request):
    aquariums = Aquariums.objects.filter(user=request.user).only('id', 'user', 'name', 'size', 'type', 'start_date')
    
    if request.method == "POST":
        form = AddAquariumForm(request.POST)
        if form.is_valid():
            aquarium = form.save(commit=False)
            aquarium.user = request.user
            aquarium.save()
            return redirect("accounts:home")  # prevent form resubmission
    else:
        form = AddAquariumForm()
    
    recent_params = WaterParameter.objects.filter(aquarium__user=request.user).order_by('-measured_at')[:5]
    recent_livestock = Livestock.objects.filter(user=request.user).order_by('-date_acquired')[:5]
    recent_photos = Photo.objects.filter(aquarium__user=request.user).order_by('-created_at')[:5]
    
    activity_list = list(chain(recent_params, recent_livestock, recent_photos))    
    def get_date(item):
        if isinstance(item, WaterParameter) and item.measured_at:
            return time.mktime(item.measured_at.timetuple())
        elif isinstance(item, Livestock) and item.date_acquired:
            return time.mktime(item.date_acquired.timetuple())
        elif isinstance(item, Photo) and item.created_at:
            return time.mktime(item.created_at.timetuple())
        return 0
    
    recent_activity = sorted(activity_list, key=get_date, reverse=True)[:6]   
        
    # --- NEW ALERT LOGIC ---
    alerts = []
    
    for tank in aquariums:
        # Get the absolute newest reading for each parameter type in this tank
        latest_params = WaterParameter.objects.filter(aquarium=tank).order_by('parameter', '-measured_at').distinct('parameter')
        
        for param in latest_params:
            # Check if the user has set a target for this specific parameter
            target = ParameterTarget.objects.filter(aquarium=tank, parameter=param.parameter).first()
            
            if target:
                # If the value is outside the safe zone, trigger an alert!
                if param.value < target.min_value or param.value > target.max_value:
                    alerts.append({
                        'tank': tank.name,
                        'param_name': param.get_parameter_display(),
                        'value': param.value,
                        'unit': param.unit,
                        'min': target.min_value,
                        'max': target.max_value,
                        'is_low': param.value < target.min_value
                    })

    return render(request, "home.html", {
        "aquariums": aquariums, 
        "form": form,
        "recent_activity": recent_activity,
        "alerts": alerts  # <--- Pass the alerts to the template
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        # The 'instance' keyword tells Django to update this specific user, not create a new one!
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        # Pre-fill the form with the user's current data when they load the page
        form = UserEditForm(instance=request.user)

    return render(request, 'accounts/edit_profile.html', {'form': form})



@login_required
def profile(request):
    return render(request, "profile.html")
