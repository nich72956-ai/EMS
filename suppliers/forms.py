from django import forms
from .models import Supplier


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = [
            'supplier_code',
            'company_name',
            'contact_person',
            'phone',
            'email',
            'address',
        ]