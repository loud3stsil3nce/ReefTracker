
from django.contrib import admin
from .models import Aquariums, Livestock, Species, ParameterTarget, WaterParameter

admin.site.register(Aquariums)
admin.site.register(Livestock)
admin.site.register(Species) 
admin.site.register(WaterParameter)
admin.site.register(ParameterTarget)