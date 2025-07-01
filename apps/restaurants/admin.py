from django.contrib import admin
from .models import RestaurantModel

@admin.register(RestaurantModel)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'cuisine_type', 'created_at']
    list_filter = ['cuisine_type', 'created_at']
    search_fields = ['name', 'address', 'cuisine_type']
    readonly_fields = ['created_at', 'updated_at']