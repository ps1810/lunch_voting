from django.contrib import admin
from .models import VoteModel

@admin.register(VoteModel)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'restaurant', 'weight', 'created_at']
    list_filter = ['weight', 'created_at']
    search_fields = ['user__username', 'restaurant__name']
    readonly_fields = ['created_at']