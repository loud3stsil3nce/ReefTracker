from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm # Ensure this is moved from main to accounts/forms.py
from aquariums.models import Aquariums
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
    return render(request, "home.html", {"aquariums": aquariums, "form": form})


def sign_up(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, "sign_up.html", {"form": form})

@login_required
def profile(request):
    return render(request, "profile.html")
