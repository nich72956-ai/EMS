from django.contrib import admin
from .models import Purchase


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        'supplier',
        'product',
        'quantity',
        'buying_price',
        'purchased_at',
    )