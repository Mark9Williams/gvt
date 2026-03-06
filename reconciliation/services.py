from django.db.models import Sum
from sales.models import SaleItem
from inventory.models import StockTransfer, StoreInventory


def generate_reconciliation_report(store, start_date, end_date):

    report = []

    inventory_items = StoreInventory.objects.filter(store=store)

    for item in inventory_items:

        product = item.product
        opening_stock = item.quantity

        transfers_in = StockTransfer.objects.filter(
            destin=store,
            product=product,
            transferred_At__date__range=(start_date, end_date)
        ).aggregate(total=Sum("quantity"))["total"] or 0

        transfers_out = StockTransfer.objects.filter(
            source=store,
            product=product,
            transferred_At__date__range=(start_date, end_date)
        ).aggregate(total=Sum("quantity"))["total"] or 0

        sales = SaleItem.objects.filter(
            sale__store=store,
            product=product,
            sale__created_at__date__range=(start_date, end_date)
        ).aggregate(total=Sum("quantity"))["total"] or 0

        expected_stock = opening_stock + transfers_in - transfers_out - sales

        actual_stock = item.quantity

        variance = actual_stock - expected_stock

        report.append({
            "product_id": product.id,
            "product_name": product.name,
            "opening_stock": opening_stock,
            "transfers_in": transfers_in,
            "transfers_out": transfers_out,
            "sales": sales,
            "expected_stock": expected_stock,
            "actual_stock": actual_stock,
            "variance": variance
        })

    return report