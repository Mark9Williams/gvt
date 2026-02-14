from django.db import models
from user.models import User
from store.models import Store

# Create your models here.
class StoreAssignment(models.Model):
    user = models.OneToOneField(User, on_delete= models.PROTECT, related_name='storeuser')
    store = models.ForeignKey(Store, on_delete= models.CASCADE)
    assigned_At = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} with {self.store.name}"