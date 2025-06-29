from django.contrib import admin

# Register your models here.
from .models import Aquariums, CalciumProducts

admin.site.register(Aquariums)
admin.site.register(CalciumProducts)