from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.conf import settings


# Create your models here.
class CalciumProducts(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    PPMPerLiter = models.FloatField(help_text="PPM per liter of solution")
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
    

class MagnesiumProducts(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    PPMPerLiter = models.FloatField(help_text="PPM per liter of solution")
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
    