from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UserEditForm
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
