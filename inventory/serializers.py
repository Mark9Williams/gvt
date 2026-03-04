from django.db import transaction
from rest_framework import serializers
from .models import StoreInventory, StockTransfer


class StoreInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreInventory
        fields = "__all__"


class StockTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockTransfer
        fields = "__all__"

    def create(self, validated_data):
        with transaction.atomic():
            transfer = StockTransfer.objects.create(**validated_data)

            product = transfer.product
            quantity = transfer.quantity

            # Deduct from source store (if exists)
            if transfer.source:
                source_inventory = StoreInventory.objects.select_for_update().get(
                    store=transfer.source,
                    product=product
                )

                if source_inventory.quantity < quantity:
                    raise serializers.ValidationError("Insufficient source stock")

                source_inventory.quantity -= quantity
                source_inventory.save()

            # Add to destination store
            dest_inventory = StoreInventory.objects.select_for_update().get_or_create(
                store=transfer.destin,
                product=product,
                defaults={"quantity": 0}
            )

            dest_inventory.quantity += quantity
            dest_inventory.save()

        return transfer