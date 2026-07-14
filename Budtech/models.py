from django.db import models


class CompanyProfile(models.Model):

    name = models.CharField(max_length=200)

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.name