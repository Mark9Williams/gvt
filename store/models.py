from django.db import models

# Create your models here.
class Store(models.Model):
    name = models.CharField(max_length=50, null=False)
    location = models.CharField(max_length=50, null=False)
    address = models.TextField(max_length=100)
    created_At = models.DateTimeField(auto_now_add=True)
    updated_At = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} located in {self.location}"
