from django.db import models
from store.models import Store
from product.models import Product

# Create your models here.
class StoreInventory(models.Model):
    store = models.ForeignKey(Store, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=0.0)
    created_At = models.DateTimeField(auto_now_add=True)
    updated_At = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} at {self.store.name} has {self.quantity}"


class StockTransfer(models.Model):
    source = models.ForeignKey(Store, null=True, blank=True, on_delete=models.SET_NULL,related_name="outgoing_transfers")
    destin = models.ForeignKey(Store, on_delete=models.CASCADE, null = True, related_name="incoming_transfers")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=0.0)
    price = models.PositiveIntegerField(default=1)
    transferred_At = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" Transffered {self.quantity} of {self.product.name} from {self.source.name} to {self.destination.name}"
    