from django.db import transaction
from .models import Sale,SaleItem
from inventory.models import StoreInventory
from rest_framework import serializers

class SaleItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = SaleItem
        fields = [
            "id",
            "product",
            "product_name",
            "quantity",
            "unit_price",
            "total_price"
        ]

    def get_total_price(self, obj):
        return obj.quantity * obj.unit_price


class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True, write_only=True)
    sale_items = SaleItemSerializer(source="saleitem_set", many=True, read_only=True)

    seller_name = serializers.CharField(source="seller.username", read_only=True)
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = [
            "id",
            "store",
            "seller",
            "seller_name",
            "route_taken",
            "vehicle_number",
            "created_at",
            "items",
            "sale_items",
            "total_amount"
        ]
        read_only_fields = ["seller", "created_at"]

    def get_total_amount(self, obj):
        items = obj.saleitem_set.all()
        return sum(i.quantity * i.unit_price for i in items)

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
