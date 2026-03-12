from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Count
from django.db.models.functions import TruncDate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.dateparse import parse_date

from sales.models import SaleItem
from inventory.models import StoreInventory
# from core.permissions import IsManager


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        start_date = parse_date(request.GET.get("start_date")) if request.GET.get("start_date") else None
        end_date = parse_date(request.GET.get("end_date")) if request.GET.get("end_date") else None
        store_id = request.GET.get("store")

        sale_items = SaleItem.objects.select_related(
            "sale", "product", "sale__store", "sale__seller"
        )

        # Apply filters
        if start_date and end_date:
            sale_items = sale_items.filter(
                sale__created_at__date__range=(start_date, end_date)
            )

        if store_id:
            sale_items = sale_items.filter(
                sale__store_id=store_id
            )

        revenue_expression = ExpressionWrapper(
            F("quantity") * F("unit_price"),
            output_field=DecimalField(max_digits=15, decimal_places=2)
        )

        #Revenue per store
        revenue_per_store = sale_items.values(
            "sale__store__id",
            "sale__store__name"
        ).annotate(
            total_revenue=Sum(revenue_expression)
        ).order_by("-total_revenue")

        #Revenue per seller
        revenue_per_seller = sale_items.values(
            "sale__seller__id",
            "sale__seller__username"
        ).annotate(
            total_revenue=Sum(revenue_expression)
        ).order_by("-total_revenue")

        #Top selling products
        top_products = sale_items.values(
            "product__id",
            "product__name"
        ).annotate(
            total_quantity=Sum("quantity"),
            total_revenue=Sum(revenue_expression)
        ).order_by("-total_quantity")[:10]

        #Low stock alerts (threshold = 10)
        LOW_STOCK_THRESHOLD = 10

        low_stock = StoreInventory.objects.filter(
            quantity__lte=LOW_STOCK_THRESHOLD
        ).values(
            "store__id",
            "store__name",
            "product__id",
            "product__name",
            "quantity"
        )

        #Daily sales trend
        daily_trend = sale_items.annotate(
            date=TruncDate("sale__created_at")
        ).values("date").annotate(
            total_revenue=Sum(revenue_expression),
            total_quantity=Sum("quantity")
        ).order_by("date")

        # convert querysets to lists to ensure they are serialized
        return Response({
            "revenue_per_store": list(revenue_per_store),
            "revenue_per_seller": list(revenue_per_seller),
            "top_selling_products": list(top_products),
            "low_stock_alerts": list(low_stock),
            "daily_sales_trend": list(daily_trend),
        })