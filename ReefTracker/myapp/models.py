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
    
  
  
  
  
  
        
class CalciumProducts(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    PPMPerLiter = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    

class MagnesiumProducts(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    PPMPerLiter = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name 
    
    