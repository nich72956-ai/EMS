from django.db import models
from suppliers.models import Supplier
from products.models import Product


class Purchase(models.Model):
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()

    buying_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    purchased_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.product.name} from {self.supplier.company_name}"