from django.db import models
from brand.models import Brand

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=70)
    brand = models.ForeignKey(Brand, on_delete= models.CASCADE)
    created_At = models.DateTimeField(auto_now_add=True)
    updated_At = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} with {self.brand.name}"
    
