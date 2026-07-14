from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "serial_number",
            "barcode",
            "name",
            "category",
            "buying_price",
            "selling_price",
            "quantity_in_stock",
            "reorder_level",
        ]