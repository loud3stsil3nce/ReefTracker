from django.shortcuts import render, HttpResponse
from .models import Aquariums
# Create your views here.
from .forms import RegisterForm, LoginForm, WaterVolumeFormImperial, WaterVolumeFormMetric

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
    result = "5"
    form_unit = request.POST.get("form_unit", "imperial")
    if request.method == "POST":
        if form_unit == "imperial":
            form = WaterVolumeFormImperial(request.POST)
        else:
            form = WaterVolumeFormMetric(request.POST)
        if form.is_valid():
            #add data processing logic here
            result = "5"
            return render(request, "watervolume.html", {"form_unit": form_unit, "form": form})
    else:
        form = WaterVolumeFormImperial() if form_unit == "imperial" else WaterVolumeFormMetric()
    return render(request, "watervolume.html", {"form_unit": form_unit, "form": form, "result": result})
        