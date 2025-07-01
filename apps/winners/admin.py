from django.contrib import admin
from .models import DailyWinnerModel

@admin.register(DailyWinnerModel)
class DailyWinnerAdmin(admin.ModelAdmin):
    list_display = ['date', 'restaurant_name', 'total_score', 'unique_voters']
    list_filter = ['date']
    search_fields = ['restaurant_name']
    readonly_fields = ['created_at']