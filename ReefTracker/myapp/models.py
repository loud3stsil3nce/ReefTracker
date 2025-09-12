from django.db import models
from django.contrib.auth.models import User
from datetime import date
# Create your models here.


class Aquariums(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='aquariums')
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    type = models.CharField(max_length=50)  # e.g., freshwater, saltwater
    start_date = models.DateField(default=date.today)
    
  
class Livestock(models.Model):
    LIVESTOCK_TYPES = [
        ('fish', 'Fish'),
        ('coral', 'Coral'),
        ('invertebrate', 'Invertebrate'),
        ('crustacean', 'Crustacean'),
        ('mollusk', 'Mollusk'),
        ('anemone', 'Anemone'),
        ('algae', 'Algae'),
        ('sponge', 'Sponge'),
        ('urchin', 'Urchin / Echinoderm'),
        ('other', 'Other'),
    ]
    
    aquarium = models.ForeignKey(Aquariums, on_delete=models.CASCADE, related_name="livestock")
    name = models.CharField(max_length=100, help_text="Common name of the livestock")
    species = models.CharField(max_length=100, blank=True, help_text="Scientific name")
    livestock_type = models.CharField(max_length=20, choices=LIVESTOCK_TYPES, default='other')
    date_added = models.DateField(default=date.today)
    health_status = models.CharField(max_length=50, default='healthy', help_text="Current health status")
    notes = models.TextField(blank=True, help_text="Additional notes about this livestock")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_livestock_type_display()})"
    
    class Meta:
        ordering = ['-date_added']
        
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
    