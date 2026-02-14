from django.db import models
from store.models import Store
from user.models import User

# Create your models here.
class Reconciliation(models.Model):
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="reconciliations"
    )
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="reconciliations"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.store.name} ({self.start_date} - {self.end_date})"