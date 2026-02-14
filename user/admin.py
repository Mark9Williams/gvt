from .models import User
from django.contrib import admin

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id","username","email","phone","role"]
    list_filter = ["role"]
    search_fields = ["username","email","phone"]
