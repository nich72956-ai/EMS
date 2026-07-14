from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'customer_code',
        'first_name',
        'last_name',
        'phone',
        'email',
    )

    search_fields = (
        'customer_code',
        'first_name',
        'last_name',
        'phone',
    )