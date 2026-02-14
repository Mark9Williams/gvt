from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    ROLE_MANAGER = 'manager'
    ROLE_SELLER = 'seller'
    role = models.CharField(max_length=10,null=False,choices=((ROLE_MANAGER,'Manager'),(ROLE_SELLER,'Seller')))
    phone = models.CharField(max_length=10)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['role'])
        ]

    def __str__(self):
        return f"{self.role} with {self.username}"