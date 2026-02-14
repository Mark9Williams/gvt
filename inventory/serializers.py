from django.db import transaction
from rest_framework import serializers
from .models import StoreInventory,StockTransfer

class StoreInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreInventory
        fields = '__all__'



class StockTransferSerializer(serializers.ModelSerializer):
    class Meta:
            model = StockTransfer
            fields = "__all__"
            read_only_fields = ["created_by", "created_at"]
    # def create(self, validated_data):
    #         validated_data["created_by"] = self.context["request"].user
    #         return super().create(validated_data)
    def create(self, validated_data):
        user = self.context["request"].user
        with transaction.atomic():
            transfer = StockTransfer.objects.create(
                created_by=user,
                **validated_data
            )
            product = transfer.product
            quantity = transfer.quantity
            # Deduct from source store (if exists)
            if transfer.from_store:
                source_inventory = StoreInventory.objects.select_for_update().get(
                store=transfer.from_store,
                product=product
                )
                if source_inventory.quantity < quantity:
                    raise serializers.ValidationError("Insufficient source stock")
                source_inventory.quantity -= quantity
                source_inventory.save()
            # Add to destination store
            dest_inventory, created = StoreInventory.objects.select_for_update().get(
            store=transfer.to_store,
            product=product,
            defaults={"quantity": 0}
            )
            dest_inventory.quantity += quantity
            dest_inventory.save()
        return transfer