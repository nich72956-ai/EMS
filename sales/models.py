from django.db import models
from customers.models import Customer


class Sale(models.Model):

    PAYMENT_CHOICES = [
        ("Cash", "Cash"),
        ("M-Pesa", "M-Pesa"),
        ("Card", "Card"),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default="Cash"
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale {self.id}"