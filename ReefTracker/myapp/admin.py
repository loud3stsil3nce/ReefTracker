from django.contrib import admin


from .models import Aquariums, CalciumProducts, MagnesiumProducts, Livestock, Photo, WaterParameter

admin.site.register(Aquariums)
admin.site.register(CalciumProducts)
admin.site.register(MagnesiumProducts)
admin.site.register(Livestock)
admin.site.register(Photo)
admin.site.register(WaterParameter)