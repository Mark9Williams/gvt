from django.db import models
from store.models import Store
from user.models import User
from product.models import Product

# Create your models here.
class Sale(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.PROTECT)
    route_taken = models.CharField(max_length=255)
    vehicle_number = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class SaleItem(models.Model):
    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12,decimal_places=2)

    def __str__(self):
        return super().__str__()
    

