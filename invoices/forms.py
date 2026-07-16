from django import forms
from .models import Invoice, InvoiceItem


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ["customer"]


class InvoiceItemForm(forms.ModelForm):
    barcode = forms.CharField(
        required=False,
        label="Scan Barcode",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Scan barcode here...",
                "autofocus": True,
            }
        ),
    )

    class Meta:
        model = InvoiceItem
        fields = [
            "barcode",
            "product",
            "quantity",
        ]

        widgets = {
            "product": forms.Select(
                attrs={"class": "form-control"}
            ),
            "quantity": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
        }