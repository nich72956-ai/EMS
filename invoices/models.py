from django.db import models
from customers.models import Customer
from products.models import Product


class Invoice(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True)

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.invoice_number

    def total_amount(self):
        return sum(item.total_price() for item in self.items.all())


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.product.name} - {self.invoice.invoice_number}"