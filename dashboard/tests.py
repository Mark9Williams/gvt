from django.test import TestCase
from rest_framework.test import APIClient
from user.models import User
from store.models import Store
from product.models import Product
from sales.models import Sale, SaleItem
from inventory.models import StoreInventory


class DashboardViewTests(TestCase):
    def setUp(self):
        # create a manager user
        self.manager = User.objects.create_user(
            username="mgr", password="pass", role=User.ROLE_MANAGER
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.manager)

        # create some data
        self.store = Store.objects.create(name="Test Store", address="123")
        self.product = Product.objects.create(name="Widget", price=10)
        # sale with one item
        sale = Sale.objects.create(store=self.store, seller=self.manager, route_taken="r1", vehicle_number="v1")
        SaleItem.objects.create(sale=sale, product=self.product, quantity=2, unit_price=10)
        # low stock inventory
        StoreInventory.objects.create(store=self.store, product=self.product, quantity=5)

    def test_dashboard_endpoint(self):
        response = self.client.get("/api/dashboard/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # check expected keys exist
        expected_keys = [
            "revenue_per_store",
            "revenue_per_seller",
            "top_selling_products",
            "low_stock_alerts",
            "daily_sales_trend",
        ]
        for key in expected_keys:
            self.assertIn(key, data)
        # basic sanity on data types
        self.assertIsInstance(data["revenue_per_store"], list)
        self.assertIsInstance(data["low_stock_alerts"], list)
