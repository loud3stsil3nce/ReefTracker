from django.shortcuts import render, HttpResponse
from .models import Aquariums
# Create your views here.
from .forms import RegisterForm, LoginForm

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