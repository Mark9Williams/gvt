from django.contrib import admin
from .models import StoreAssignment

# Register your models here.
@admin.register(StoreAssignment)
class StoreAssignmentAdmin(admin.ModelAdmin):
    list_display = ['store','user','assigned_At']
    list_filter = ['store','user']
    search_fields  = ['store','user']

