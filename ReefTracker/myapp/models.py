from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.conf import settings

# Create your models here.


class Aquariums(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='aquariums')
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    type = models.CharField(max_length=50)  # e.g., freshwater, saltwater
    start_date = models.DateField(default=date.today)
    volume_liters = models.FloatField(null=True, blank=True, help_text="Net water volume in liters")

class Species(models.Model):
    CATEGORY_CHOICES = [
        ('FISH', 'Fish'),
        ('CORAL', 'Coral'),
        ('INVERT', 'Invertebrate'),
        ('MACRO', 'Macroalgae'),
    ]
    
    common_name = models.CharField(max_length=40)
    scientific_name = models.CharField(max_length=40, blank=True, null=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    
    class Meta:
        verbose_name_plural = "Species"
        ordering = ['category', 'common_name']
        
    def __str__(self):
        return f"{self.common_name} ({self.get_category_display()})" 
  
class Livestock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    species = models.ForeignKey(Species, on_delete=models.SET_NULL, null=True, related_name='livestock_instances')
    
    # If the user has something rare not in your DB, they can type a custom name
    custom_name = models.CharField(max_length=100, blank=True, null=True, help_text="Use this if species is not in the list")
    
    date_acquired = models.DateField()
    notes = models.TextField(blank=True)
    
    # Image handling (assuming you have Pillow installed)
    image = models.ImageField(upload_to='livestock_images/', blank=True, null=True)

    def __str__(self):
        if self.species:
            return f"{self.species.common_name} - {self.user.username}"
        return f"{self.custom_name} - {self.user.username}"
      
      
      
      
        
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
    

class WaterParameter(models.Model):
    PARAMETER_PH = 'ph'
    PARAMETER_TEMP = 'temp'
    PARAMETER_SALINITY = 'salinity'
    PARAMETER_DKH = 'dkh'
    PARAMETER_CALCIUM = 'calcium'
    PARAMETER_MAGNESIUM = 'magnesium'
    PARAMETER_NITRATE = 'nitrate'
    PARAMETER_PHOSPHATE = 'phosphate'
    PARAMETER_AMMONIA = 'ammonia'
    PARAMETER_NITRITE = 'nitrite'

    PARAMETER_CHOICES = [
        (PARAMETER_PH, 'pH'),
        (PARAMETER_TEMP, 'Temperature'),
        (PARAMETER_SALINITY, 'Salinity'),
        (PARAMETER_DKH, 'Alkalinity (dKH)'),
        (PARAMETER_CALCIUM, 'Calcium'),
        (PARAMETER_MAGNESIUM, 'Magnesium'),
        (PARAMETER_NITRATE, 'Nitrate (NO3)'),
        (PARAMETER_PHOSPHATE, 'Phosphate (PO4)'),
        (PARAMETER_AMMONIA, 'Ammonia (NH3/NH4+)'),
        (PARAMETER_NITRITE, 'Nitrite (NO2-)'),
    ]

    # Allowed units per parameter. Validation will ensure the selected unit matches the parameter.
    ALLOWED_UNITS_BY_PARAMETER = {
        PARAMETER_PH: [
            ('pH', 'pH'),
        ],
        PARAMETER_TEMP: [
            ('C', '°C'),
            ('F', '°F'),
        ],
        PARAMETER_SALINITY: [
            ('sg', 'Specific Gravity (sg)'),
            ('ppt', 'Parts per Thousand (ppt)'),
            ('psu', 'Practical Salinity Units (PSU)'),
        ],
        PARAMETER_DKH: [
            ('dKH', 'dKH'),
            ('meq/L', 'meq/L'),
            ('ppm', 'ppm as CaCO3'),
        ],
        PARAMETER_CALCIUM: [
            ('ppm', 'ppm (mg/L)'),
        ],
        PARAMETER_MAGNESIUM: [
            ('ppm', 'ppm (mg/L)'),
        ],
        PARAMETER_NITRATE: [
            ('ppm', 'ppm (mg/L)'),
            ('mg/L', 'mg/L'),
        ],
        PARAMETER_PHOSPHATE: [
            ('ppm', 'ppm (mg/L)'),
            ('mg/L', 'mg/L'),
        ],
        PARAMETER_AMMONIA: [
            ('ppm', 'ppm (mg/L)'),
            ('mg/L', 'mg/L'),
        ],
        PARAMETER_NITRITE: [
            ('ppm', 'ppm (mg/L)'),
            ('mg/L', 'mg/L'),
        ],
    }

    aquarium = models.ForeignKey(Aquariums, on_delete=models.CASCADE, related_name='parameters')
    parameter = models.CharField(max_length=20, choices=PARAMETER_CHOICES)
    value = models.FloatField()
    unit = models.CharField(max_length=20, help_text="Measurement unit, validated against parameter type")
    measured_at = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        allowed = dict(self.ALLOWED_UNITS_BY_PARAMETER).get(self.parameter)
        # dict(...) above would only keep last value for duplicate keys; use direct mapping
        allowed = self.ALLOWED_UNITS_BY_PARAMETER.get(self.parameter, [])
        allowed_values = {code for code, _ in allowed}
        if self.unit not in allowed_values:
            readable = ', '.join(code for code in allowed_values) or 'None'
            raise ValidationError({
                'unit': f"Unit '{self.unit}' is not valid for parameter '{self.parameter}'. Allowed: {readable}"
            })

    def __str__(self):
        return f"{self.get_parameter_display()} {self.value} {self.unit} @ {self.measured_at:%Y-%m-%d}"

    class Meta:
        ordering = ['-measured_at']
        indexes = [
            models.Index(fields=['aquarium', 'parameter', 'measured_at']),
        ]
        
        
class Photo(models.Model):
    aquarium = models.ForeignKey('Aquariums', on_delete=models.CASCADE, related_name='photos')
    livestock = models.ForeignKey('Livestock', on_delete=models.SET_NULL, null=True, blank=True, related_name='photos')
    
    # This will store the image in a folder like 'uploads/photos/user_1/'
    image = models.ImageField(upload_to='photos/')
    caption = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Photo for {self.aquarium.name} on {self.created_at.strftime('%Y-%m-%d')}"