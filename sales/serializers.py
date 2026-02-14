from django.db import transaction
from .models import Sale,SaleItem
from inventory.models import StoreInventory
from rest_framework import serializers

class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = ["id", "product", "quantity", "unit_price"]


class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many =True, write_only =True)
    # sale_items = SaleItemSerializer(source ="items", many=True, read_only=True)
    class Meta:
        model = Sale
        fields = [
            "id",
            "store",
            "seller",
            "route_taken",
            "vehicle_number",
            "created_at",
            "items",
            # "sale_items",
        ]
        read_only_fields = ["seller", "created_at"]

    def create(self,validated_data):
        items_data = validated_data.pop("items")
        user = self.context["request"].user

        with transaction.atomic():
            sale = Sale.objects.create(
                seller=user,
                **validated_data
            )
            for item in items_data:
                inventory = StoreInventory.objects.select_for_update().get(
                    store=sale.store,
                    product=item["product"]
                )

                if inventory.quantity < item["quantity"]:
                    raise serializers.ValidationError(f"Not enough stock for {item['product'].name}")
                
                inventory.quantity -= item["quantity"]
                inventory.save()

                SaleItem.objects.create(
                    sale=sale,
                    **item
                )
            return sale

        # sale = Sale.objects.create(
        #     seller= user
        #     **validated_data
        # )

        # for item in items_data:
        #     SaleItem.objects.create(sale=sale,**item)
        # return sale
