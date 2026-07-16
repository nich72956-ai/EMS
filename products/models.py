from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    # Product Identification
    sku = models.CharField(
        max_length=30,
        unique=True,
        blank=True
    )

    serial_number = models.CharField(
        max_length=100,
        unique=True
    )

    barcode = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True
    )

    # Product Information
    name = models.CharField(max_length=200)

    brand = models.CharField(
        max_length=100,
        blank=True
    )

    UNIT_CHOICES = [
        ("Piece", "Piece"),
        ("Box", "Box"),
        ("Carton", "Carton"),
        ("Pack", "Pack"),
        ("Bottle", "Bottle"),
        ("Kg", "Kilogram"),
        ("Gram", "Gram"),
        ("Litre", "Litre"),
        ("Metre", "Metre"),
    ]

    unit = models.CharField(
        max_length=20,
        choices=UNIT_CHOICES,
        default="Piece"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    # Pricing
    buying_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    selling_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # Inventory
    quantity_in_stock = models.PositiveIntegerField(default=0)

    reorder_level = models.PositiveIntegerField(default=10)

    # Product Image
    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.barcode})"