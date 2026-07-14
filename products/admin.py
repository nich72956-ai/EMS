from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'serial_number',
        'name',
        'category',
        'buying_price',
        'selling_price',
        'quantity_in_stock',
    )

    search_fields = (
        'serial_number',
        'barcode',
        'name',
    )

    list_filter = (
        'category',
    )