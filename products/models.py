from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    serial_number = models.CharField(max_length=100, unique=True)
    barcode = models.CharField(max_length=100, blank=True, null=True)

    name = models.CharField(max_length=200)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    buying_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    selling_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    quantity_in_stock = models.PositiveIntegerField(default=0)

    reorder_level = models.PositiveIntegerField(default=10)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name