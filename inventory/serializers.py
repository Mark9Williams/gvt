from django.db import transaction
from rest_framework import serializers
from .models import StoreInventory, StockTransfer


class StoreInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreInventory
        fields = "__all__"

    @transaction.atomic
    def create(self, validated_data):
        """Ensure only one record per store/product and increment quantity.

        When a new StoreInventory is created using this serializer, we look for an
        existing instance for the same store/product combination. If one exists
        we add the incoming quantity to the existing record instead of creating
        a duplicate.  The database has a unique_together constraint as a safety
        net, but this logic avoids IntegrityErrors and makes the API behavior
        intuitive to clients.
        """
        store = validated_data["store"]
        product = validated_data["product"]
        quantity = validated_data.get("quantity", 0)

        inventory, created = StoreInventory.objects.select_for_update().get_or_create(
            store=store,
            product=product,
            defaults={"quantity": quantity},
        )

        if not created:
            inventory.quantity += quantity
            inventory.save()
        return inventory

class StockTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockTransfer
        fields = "__all__"

    def create(self, validated_data):
        with transaction.atomic():
            transfer = StockTransfer.objects.create(**validated_data)

            product = transfer.product
            quantity = transfer.quantity

            # Deduct from source store
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
            dest_inventory, created = StoreInventory.objects.select_for_update().get_or_create(
                store=transfer.destin,
                product=product,
                defaults={"quantity": 0}
            )

            dest_inventory.quantity += quantity
            dest_inventory.save()

        return transfer