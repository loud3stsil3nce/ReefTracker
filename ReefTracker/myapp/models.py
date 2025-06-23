from django.db import models

# Create your models here.


class Aquariums(models.Model):
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    type = models.CharField(max_length=50)  # e.g., freshwater, saltwater
    created_at = models.DateTimeField(auto_now_add=True)

    