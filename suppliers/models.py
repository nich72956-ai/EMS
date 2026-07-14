from django.db import models


class Supplier(models.Model):
    supplier_code = models.CharField(max_length=20, unique=True)
    company_name = models.CharField(max_length=200)

    contact_person = models.CharField(max_length=150)

    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)

    address = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.supplier_code} - {self.company_name}"