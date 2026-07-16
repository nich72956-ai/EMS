from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
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
            "image",
        ]

        widgets = {
            "barcode": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Scan or enter barcode",
                "autofocus": True,
            }),

            "serial_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Scan or enter serial number",
            }),

            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Product name",
            }),

            "brand": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Brand",
            }),

            "category": forms.Select(attrs={
                "class": "form-control",
            }),

            "unit": forms.Select(attrs={
                "class": "form-control",
            }),

            "buying_price": forms.NumberInput(attrs={
                "class": "form-control",
            }),

            "selling_price": forms.NumberInput(attrs={
                "class": "form-control",
            }),

            "quantity_in_stock": forms.NumberInput(attrs={
                "class": "form-control",
            }),

            "reorder_level": forms.NumberInput(attrs={
                "class": "form-control",
            }),

            "image": forms.ClearableFileInput(attrs={
                "class": "form-control",
            }),
        }

    def clean_barcode(self):
        barcode = self.cleaned_data.get("barcode")

        if barcode:
            exists = Product.objects.filter(barcode=barcode)

            if self.instance.pk:
                exists = exists.exclude(pk=self.instance.pk)

            if exists.exists():
                raise forms.ValidationError(
                    "This barcode already exists."
                )

        return barcode

    def clean_serial_number(self):
        serial = self.cleaned_data.get("serial_number")

        exists = Product.objects.filter(serial_number=serial)

        if self.instance.pk:
            exists = exists.exclude(pk=self.instance.pk)

        if exists.exists():
            raise forms.ValidationError(
                "This serial number already exists."
            )

        return serial