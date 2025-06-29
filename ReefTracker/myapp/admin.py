from django.contrib import admin

# Register your models here.
from .models import Aquariums, CalciumProducts, MagnesiumProducts

admin.site.register(Aquariums)
admin.site.register(CalciumProducts)
admin.site.register(MagnesiumProducts)