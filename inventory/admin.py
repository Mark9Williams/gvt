from django.contrib import admin
from .models import StoreInventory,StockTransfer

# Register your models here.
@admin.register(StoreInventory)
class StoreInventoryAdmin(admin.ModelAdmin):
    list_display = ['store','product','quantity','created_At','updated_At']
    list_filter = ['store','product','created_At']
    search_fields = ['store','product']


@admin.register(StockTransfer)
class StockTransferAdmin(admin.ModelAdmin):
    list_display = ['source','destin','product','quantity','price','transferred_At']
    list_filter = ['source','destin','product','transferred_At']
    search_fields = ['source','destin','product']