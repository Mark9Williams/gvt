from django.db import models

# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=30)
    created_At = models.DateTimeField(auto_now_add=True)
    updated_At = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
