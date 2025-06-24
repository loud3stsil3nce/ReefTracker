from django.shortcuts import render, HttpResponse
from .models import Aquariums
# Create your views here.


def home(request):
    return render(request, "home.html")

def login(request):
    return render(request, "login.html")


def register(request):
    return render(request, "register.html")


def profile(request):
    return render(request, "profile.html")

def calculators(request):
    return render(request, "displaycalculators.html")

def myaquariums(request):
    tanks = Aquariums.objects.all()
    return render(request, "myaquariums.html", {"aquariums": tanks})