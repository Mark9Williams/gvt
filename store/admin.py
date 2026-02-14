from django.contrib import admin
from .models import Store

# Register your models here.
@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['id','name','location','address']
    list_filter = ['location','created_At']
    search_fields = ['name','location']
