from django.contrib import admin
from .models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):

    list_display = (
        'supplier_code',
        'company_name',
        'contact_person',
        'phone',
        'email',
    )

    search_fields = (
        'supplier_code',
        'company_name',
        'contact_person',
    )