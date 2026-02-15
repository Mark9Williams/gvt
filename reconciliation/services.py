from django.db.models import Sum
from sales.models import SaleItem
from inventory.models import StockTransfer,StoreInventory

def generate_reconciliation_report(store, start_date, end_date):
    stock_added = StockTransfer.objects.filter(
        to_store=store,
        dispatched_at__date__range=(start_date, end_date)
    ).values("product__name").annotate(
        total_added=Sum("quantity")
    )
    stock_removed = StockTransfer.objects.filter(
        from_store=store,
        dispatched_at__date__range=(start_date, end_date)
    ).values("product__name").annotate(
        total_removed=Sum("quantity")
    )
    sold = SaleItem.objects.filter(
        sale__store=store,
        sale__created_at__date__range=(start_date, end_date)
    ).values("product__name").annotate(
        total_sold=Sum("quantity")
    )
    current_inventory = StoreInventory.objects.filter(
        store=store
    )
    return {
        "stock_added": stock_added,
        "stock_removed": stock_removed,
        "sold": sold,
        "current_inventory": current_inventory
    }