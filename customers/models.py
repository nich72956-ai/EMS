from django.db import models


class Customer(models.Model):
    customer_code = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)

    address = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_code} - {self.first_name} {self.last_name}"