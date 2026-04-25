from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'client',
        'actor',
        'status',
        'total_price',
        'deadline',
        'created_at'
    )
    list_filter = ('status',)
    search_fields = ('title', 'client__username', 'actor__user__username')