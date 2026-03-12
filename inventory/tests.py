from django.test import TestCase
from django.db import IntegrityError
from .models import StoreInventory
from .serializers import StoreInventorySerializer
from store.models import Store
from product.models import Product


class StoreInventorySerializerTests(TestCase):
    def setUp(self):
        self.store = Store.objects.create(name="Main Store")
        self.product = Product.objects.create(name="Widget")

    def test_create_new_inventory(self):
        data = {"store": self.store.id, "product": self.product.id, "quantity": 10}
        serializer = StoreInventorySerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        inventory = serializer.save()
        self.assertEqual(inventory.quantity, 10)
        # only one record exists
        self.assertEqual(StoreInventory.objects.count(), 1)

    def test_create_existing_inventory_adds_quantity(self):
        # first create
        StoreInventory.objects.create(store=self.store, product=self.product, quantity=5)
        data = {"store": self.store.id, "product": self.product.id, "quantity": 7}
        serializer = StoreInventorySerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        inventory = serializer.save()
        # quantity should have been incremented rather than new record
        self.assertEqual(inventory.quantity, 12)
        self.assertEqual(StoreInventory.objects.count(), 1)

    def test_unique_constraint_prevents_manual_duplicate(self):
        StoreInventory.objects.create(store=self.store, product=self.product, quantity=3)
        with self.assertRaises(IntegrityError):
            # bypass serializer to trigger DB constraint
            StoreInventory.objects.create(store=self.store, product=self.product, quantity=4)
