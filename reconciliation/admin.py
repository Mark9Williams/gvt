from django.contrib import admin
from .models import Reconciliation

# Register your models here.
@admin.register(Reconciliation)
class ReconcileAdmin(admin.ModelAdmin):
    list_display = ['store','created_by','start_date','end_date']
    list_filter = ['store','created_by']
    search_fields = ['store','created_by','start_date']