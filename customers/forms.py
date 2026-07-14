from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'customer_code',
            'first_name',
            'last_name',
            'phone',
            'email',
            'address',
        ]