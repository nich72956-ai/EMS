from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "barcode",
        "serial_number",
        "name",
        "brand",
        "category",
        "unit",
        "buying_price",
        "selling_price",
        "quantity_in_stock",
        "reorder_level",
    )

    search_fields = (
        "barcode",
        "serial_number",
        "name",
        "brand",
    )

    list_filter = (
        "category",
        "brand",
        "unit",
    )

    ordering = ("name",)

    list_per_page = 20