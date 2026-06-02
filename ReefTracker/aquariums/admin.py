
from django.contrib import admin
from .models import Aquariums, Livestock, Species, ParameterTarget, WaterParameter, Photo, Tag

admin.site.register(Aquariums)
admin.site.register(Livestock)
admin.site.register(Species) 
admin.site.register(WaterParameter)
admin.site.register(ParameterTarget)
admin.site.register(Tag)
admin.site.register(Photo)
