from django.contrib import admin
from .models import Brand

#Register your models here.
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display =['id','name']
    search_fields = ["id","name"]
    list_filter = ['name']
